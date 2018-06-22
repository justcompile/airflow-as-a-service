import logging
import urllib3
from time import sleep

from airflow_aas.celery import app
from core.models import (
    Cluster,
    ClusterEvent,
)
from core.services.image_builder import ImageBuilder
from core.services.kube import K8sService
from core.utils.password import password_generator

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@app.task
def create_auth_proxy(clusterId):
    cluster = Cluster.objects.get(pk=clusterId)
    k8s = K8sService()

    logging.info('Creating Proxy: %s', cluster.name)

    creds = {
        'username': cluster.owner.username,
        'password': password_generator(),
        'cluster_id': clusterId,
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
def create_messagequeue(clusterId):
    cluster = Cluster.objects.get(pk=clusterId)
    k8s = K8sService()

    cluster.status = 'Creating Airflow Message Queue...'
    cluster.save()

    k8s.create_messagequeue(cluster)


@app.task
def create_webserver(clusterId):
    cluster = Cluster.objects.get(pk=clusterId)
    k8s = K8sService()

    cluster.status = 'Creating Airflow Webserver...'
    cluster.save()

    k8s.create_webserver(cluster)

    create_auth_proxy.delay(clusterId)


@app.task
def create_airflow_entity(clusterId, entity_name, requires_service=False):
    cluster = Cluster.objects.get(pk=clusterId)
    k8s = K8sService()

    k8s.create_airflow_entity(cluster, entity_name, requires_service=requires_service)


@app.task
def build_airflow_image(clusterId):
    cluster = Cluster.objects.get(pk=clusterId)

    k8s = K8sService()
    secret = k8s.get_secret(cluster)

    cluster.status = 'Grabbing the files...'
    cluster.save()

    image_builder = ImageBuilder('localhost:5000')
    image_builder.build_and_publish(cluster, secret)

    create_webserver.delay(clusterId)
    create_airflow_entity.delay(clusterId, 'scheduler')
    create_airflow_entity.delay(clusterId, 'worker', requires_service=True)
    create_airflow_entity.delay(clusterId, 'flower', requires_service=True)


@app.task
def poll_for_db(clusterId):
    cluster = Cluster.objects.get(pk=clusterId)
    sleep(10)

    cluster.status = 'Airflow Meta DB provisioned...'
    cluster.save()

    sleep(10)

    build_airflow_image.delay(clusterId)


@app.task
def create_db(clusterId):
    cluster = Cluster.objects.get(pk=clusterId)
    k8s = K8sService()

    logging.info('Creating DB for cluster %s', cluster.name)
    response = k8s.create_database(cluster)
    endpoint = k8s.client.endpoint_for_service(response)
    logging.info('MetaDB Endpoint: %s', endpoint)
    cluster.status = 'initialising Airflow Meta DB'
    cluster.save()

    poll_for_db.delay(clusterId)
    create_messagequeue.delay(clusterId)


@app.task
def init_cluster(clusterId):
    cluster = Cluster.objects.get(pk=clusterId)
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

    create_db.delay(clusterId)


@app.task
def delete_auth_proxy(clusterName):
    k8s = K8sService()
    logging.info('Deleting Namespace: %s', clusterName)

    k8s.delete_namespace(clusterName)

    return f'Deleted: {clusterName}'
