import logging
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
from core.services.git import GitClient
from core.services.image_builder import ImageBuilder
from core.services.kube import K8sService
from core.utils.password import password_generator

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
def create_webserver(cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    k8s = K8sService()

    cluster.status = 'Creating Airflow Webserver...'
    cluster.save()

    k8s.create_webserver(cluster)

    create_auth_proxy.delay(cluster_id)


@app.task
def create_airflow_entity(cluster_id, entity_name, requires_service=False):
    cluster = Cluster.objects.get(pk=cluster_id)
    k8s = K8sService()

    k8s.create_airflow_entity(cluster, entity_name, requires_service=requires_service)


# @app.task
# def build_airflow_image(cluster_id):
#     cluster = Cluster.objects.get(pk=cluster_id)

#     k8s = K8sService()
#     secret = k8s.get_secret(cluster)

#     cluster.status = 'Grabbing the files...'
#     cluster.save()

#     image_builder = ImageBuilder(settings.DOCKER_REGISTRY)
#     image_builder.build_and_publish(cluster, secret)

#     create_webserver.delay(cluster_id)
#     create_airflow_entity.delay(cluster_id, 'scheduler')
#     create_airflow_entity.delay(cluster_id, 'worker', requires_service=True)
#     create_airflow_entity.delay(cluster_id, 'flower', requires_service=True)


@app.task
def poll_for_db(cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    sleep(10)

    cluster.status = 'Airflow Meta DB provisioned...'
    cluster.save()

    # build_airflow_image.delay(cluster_id)


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


@app.task
def process_git_push(build_id, cluster_id):
    k8s = K8sService()

    build = Build.objects.get(pk=build_id)
    cluster = Cluster.objects.get(pk=cluster_id)

    git = GitClient(build.repository.owner)
    try:
        git.get_key(build.repository.name)
    except KeyError:
        git.create_and_save_keys(build.repository.name)

    with tempfile.TemporaryDirectory as tmp_dir:
        build.status = 'Cloning Repo'
        build.save()
        git.checkout(build.repository.name, build.commit_id, tmp_dir)

        # copy files to dir & build Docker Image
        build.status = 'Building Image'
        build.save()

        image_builder = ImageBuilder(settings.DOCKER_REGISTRY)
        image_builder.build_and_publish(tmp_dir, cluster_id, k8s.get_secret(cluster))


    create_webserver.delay(cluster_id)
    create_airflow_entity.delay(cluster_id, 'scheduler')
    create_airflow_entity.delay(cluster_id, 'worker', requires_service=True)
    create_airflow_entity.delay(cluster_id, 'flower', requires_service=True)
