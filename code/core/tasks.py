import logging
import os
import tempfile
from time import sleep

import urllib3
from django.conf import settings

from airflow_aas.celery import app
from core.models import (
    Build,
    Cluster,
    ClusterEvent,
)
from core.contextmanagers import cd
from core.services.image_builder import ImageBuilder
from core.services.kube import K8sService
from core.utils.password import password_generator
from scm.git import GitClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@app.task
def create_auth_proxy(cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    k8s = K8sService()

    logging.info('Creating Proxy: %s', cluster.name)

    creds = {
        'username': cluster.owner.username,
        'password': password_generator(),
        'cluster_id': cluster_id,
    }

    response = k8s.create_auth_proxy(cluster.name, **creds)

    endpoint = k8s.client.endpoint_for_service(response)

    endpoint = 'http://{username}:{password}@{endpoint}'.format(endpoint=endpoint, **creds)

    logging.info('Created proxy on: %s', endpoint)

    cluster.status = 'running'
    cluster.ui_endpoint = endpoint
    cluster.save()

    ClusterEvent.objects.create(
        description='Cluster Running',
        event_type=ClusterEvent.CLUSTER_START,
        cluster=cluster
    )

    return endpoint


@app.task
def create_messagequeue(cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    k8s = K8sService()

    cluster.status = 'Creating Airflow Message Queue...'
    cluster.save()

    k8s.create_messagequeue(cluster)


@app.task
def create_webserver(cluster_id, image_name):
    cluster = Cluster.objects.get(pk=cluster_id)
    k8s = K8sService()

    cluster.status = 'Creating Airflow Webserver...'
    cluster.save()

    k8s.create_webserver(cluster, image_name)

    create_auth_proxy.delay(cluster_id)


@app.task
def create_airflow_entity(cluster_id, entity_name, image_name, requires_service=False):
    cluster = Cluster.objects.get(pk=cluster_id)
    k8s = K8sService()

    k8s.create_airflow_entity(cluster, entity_name, image_name, requires_service=requires_service)

@app.task
def update_airflow_entity(cluster_id, entity_name, image_name):
    cluster = Cluster.objects.get(pk=cluster_id)
    k8s = K8sService()

    k8s.update(cluster, entity_name, image_name)


@app.task
def process_git_push(build_id, cluster_id, create=False):
    k8s = K8sService()

    build = Build.objects.get(pk=build_id)
    cluster = Cluster.objects.get(pk=cluster_id)

    git = GitClient(build.repository.owner)
    try:
        git.get_key(build.repository.name)
    except (KeyError, TypeError):
        git.create_and_save_keys(build.repository.name)

    with tempfile.TemporaryDirectory() as tmp_dir:
        build.status = 'Cloning Repo'
        build.save()
        git.checkout(build.repository.name, build.commit_id, tmp_dir)

        # copy files to dir & build Docker Image
        build.status = 'Building Image'
        build.save()
        build_path = os.path.join(tmp_dir, build.repository.name)

        image_builder = ImageBuilder(settings.DOCKER_REGISTRY)
        image_name = image_builder.build_and_publish(
            build_path,
            cluster,
            k8s.get_secret(cluster),
            tag=f'{build.repository.name}-{build.commit_id}'
        )

    if create:
        create_webserver.delay(cluster_id, image_name)
        create_airflow_entity.delay(cluster_id, 'scheduler', image_name)
        create_airflow_entity.delay(cluster_id, 'worker', image_name, requires_service=True)
        create_airflow_entity.delay(cluster_id, 'flower', image_name, requires_service=True)
    else:
        update_airflow_entity.delay(cluster_id, 'scheduler', image_name=image_name)
        update_airflow_entity.delay(cluster_id, 'worker', image_name=image_name)
        update_airflow_entity.delay(cluster_id, 'flower', image_name=image_name)
        update_airflow_entity.delay(cluster_id, 'ui', image_name=image_name)


@app.task
def poll_for_db(cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    sleep(10)

    cluster.status = 'Airflow Meta DB provisioned...'
    cluster.save()

    git = GitClient(cluster.owner)
    build = git.create_build_for_latest_commit(cluster.repository)

    process_git_push.delay(build.id, cluster_id, create=True)


@app.task
def create_db(cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    k8s = K8sService()

    logging.info('Creating DB for cluster %s', cluster.name)
    response = k8s.create_database(cluster)
    endpoint = k8s.client.endpoint_for_service(response)
    logging.info('MetaDB Endpoint: %s', endpoint)
    cluster.status = 'initialising Airflow Meta DB'
    cluster.save()

    poll_for_db.delay(cluster_id)
    create_messagequeue.delay(cluster_id)


@app.task
def init_cluster(cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    k8s = K8sService()
    logging.info('Creating Namespace: %s', cluster.name)
    k8s.create_namespace(cluster.name)

    ClusterEvent.objects.create(
        description='Cluster Created',
        event_type=ClusterEvent.CLUSTER_START,
        cluster=cluster
    )

    cluster.status = 'initialising'
    cluster.save()

    create_db.delay(cluster_id)


@app.task
def delete_auth_proxy(clusterName):
    k8s = K8sService()
    logging.info('Deleting Namespace: %s', clusterName)

    k8s.delete_namespace(clusterName)

    return f'Deleted: {clusterName}'
