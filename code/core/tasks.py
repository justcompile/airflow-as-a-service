import logging
from airflow_aas.celery import app
from core.models import (
    Cluster,
    ClusterEvent,
)
from core.services.kube import K8sService
from core.utils.password import password_generator


@app.task
def create_auth_proxy(clusterId):
    cluster = Cluster.objects.get(pk=clusterId)
    k8s = K8sService()
    logging.info('Creating Namespace: %s', cluster.name)
    k8s.create_namespace(cluster.name)
    logging.info('Creating Proxy: %s', cluster.name)

    creds = {
        'username': cluster.owner.username,
        'password': password_generator(),
    }

    response = k8s.create_auth_proxy(cluster.name, **creds)

    endpoint = k8s.client.config.host.replace('6443', str(response.spec.ports[0].node_port))\
        .replace('https://', '')

    endpoint = 'http://{username}:{password}@{endpoint}'.format(endpoint=endpoint, **creds)

    logging.info('Created proxy on: %s', endpoint)

    cluster.status = 'running'
    cluster.ui_endpoint = endpoint
    cluster.save()

    ClusterEvent.objects.create(
        event_type=ClusterEvent.CLUSTER_START,
        cluster=cluster
    )

    return endpoint


@app.task
def delete_auth_proxy(clusterName):
    k8s = K8sService()
    logging.info('Deleting Namespace: %s', clusterName)

    k8s.delete_namespace(clusterName)

    return f'Deleted: {clusterName}'
