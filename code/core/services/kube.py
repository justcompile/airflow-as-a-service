import os
from urllib.parse import urlparse

from django.conf import settings
import kubernetes.client
from kubernetes.client.rest import ApiException

from core.contextmanagers import compile_template
from core.utils.enc import b64encode_str
from core.utils.htpasswd import HTPasswd
from core.utils.files import load_yaml


class K8sClient(object):
    def __init__(self, config_file_path=None):
        self._config = None
        self._clients = {}

        self.__version_map = {
            'v1': kubernetes.client.CoreV1Api,
            'v1beta': kubernetes.client.ExtensionsV1beta1Api,
        }

    @property
    def config(self):
        if not self._config:
            configuration = kubernetes.client.Configuration()
            configuration.api_key['authorization'] = settings.K8S['AUTH_TOKEN']
            configuration.api_key_prefix['authorization'] = 'Bearer'
            configuration.host = settings.K8S['API_URL']
            configuration.verify_ssl = False
            self._config = configuration

        return self._config

    def endpoint_for_service(self, service):
        host_url = urlparse(self.config.host)
        return self.config.host\
            .replace(str(host_url.port), str(service.spec.ports[0].node_port))\
            .replace('https://', '')

    def __getattr__(self, item):
        try:
            return self._clients[item]
        except KeyError:
            self._clients[item] = self.__version_map[item](
                kubernetes.client.ApiClient(self.config)
            )

        return self._clients[item]


class K8sService(object):
    def __init__(self, config_file_path=None):
        self.client = K8sClient(config_file_path)
        self._raise_on_error = settings.K8S['raise_on_error']

    def create_deployment_from_yaml(self, namespace, file_path):
        dep = load_yaml(file_path=file_path)

        return self._call_api(
            self.client.v1beta.create_namespaced_deployment,
            body=dep,
            namespace=f'aaas-{namespace}'
        )

    def create_namespace(self, name):
        meta = kubernetes.client.V1ObjectMeta(
            name=f'aaas-{name}',
            labels=dict(aaas='true')
        )

        body = kubernetes.client.V1Namespace(kind='Namespace', metadata=meta)
        return self._call_api(self.client.v1.create_namespace, body)

    def delete_namespace(self, name):
        namespace_name = f'aaas-{name}'

        body = kubernetes.client.V1DeleteOptions(
            grace_period_seconds=0,
            propagation_policy='Background'
        )

        return self._call_api(self.client.v1.delete_namespace, namespace_name, body)

    def create_auth_proxy(self, name, username=None, password=None, cluster_id=None):
        assert username and password, 'Must specify username and password'

        namespace_name = f'aaas-{name}'
        with open(os.path.join(settings.BASE_DIR, 'k8s_files/proxy_auth.template')) as fp:
            self._call_api(
                self.client.v1.create_namespaced_config_map,
                namespace=namespace_name,
                body=self._create_config_map(
                    name="proxy-auth-template",
                    data={"proxy_auth.template": fp.read()}
                )
            )
        self._call_api(
            self.client.v1.create_namespaced_secret,
            namespace=namespace_name,
            body=self._create_secret(
                "proxy-htpasswd-secret",
                data={".htpasswd": HTPasswd.generate(username, password, encode=True)}
            )
        )

        with compile_template('proxy_deployment.yaml', cluster_id=cluster_id) as text:
            deployment = load_yaml(data=text)

        self._call_api(self.client.v1beta.create_namespaced_deployment, body=deployment, namespace=namespace_name)

        with compile_template('proxy_service.yaml', cluster_id=cluster_id) as text:
            service = load_yaml(data=text)

        return self._call_api(
            self.client.v1.create_namespaced_service,
            namespace=namespace_name,
            body=service
        )

    def create_database(self, cluster):

        namespace_name = f'aaas-{cluster.name}'

        db_type = cluster.db_instance.db_type

        params = {
            'image': db_type.docker_image,
            'port': db_type.port,
            'container_env': cluster.db_instance.get_env_vars(),
        }

        # Create Secret containing Environment Vars
        self._call_api(
            self.client.v1.create_namespaced_secret,
            namespace=namespace_name,
            body=self._create_secret(
                f'metadb-{cluster.id}',
                data={
                    k.lower().replace('_', '-'): b64encode_str(v)
                    for k, v in params['container_env'].items()
                }
            )
        )

        with compile_template('meta_db_deployment.yaml', cluster_id=cluster.id, **params) as text:
            deployment = load_yaml(data=text)

        self._call_api(self.client.v1beta.create_namespaced_deployment, body=deployment, namespace=namespace_name)

        with compile_template('meta_db_service.yaml', cluster_id=cluster.id, **params) as text:
            service = load_yaml(data=text)

        return self._call_api(
            self.client.v1.create_namespaced_service,
            namespace=namespace_name,
            body=service
        )

    def create_messagequeue(self, cluster):
        namespace_name = f'aaas-{cluster.name}'

        with compile_template('rabbit_deployment.yaml', cluster_id=cluster.id) as text:
            deployment = load_yaml(data=text)

        self._call_api(self.client.v1beta.create_namespaced_deployment, body=deployment, namespace=namespace_name)

        with compile_template('rabbit_service.yaml', cluster_id=cluster.id) as text:
            service = load_yaml(data=text)

        self._call_api(
            self.client.v1.create_namespaced_service,
            namespace=namespace_name,
            body=service
        )

        with compile_template('rabbit_mgr_service.yaml', cluster_id=cluster.id) as text:
            service = load_yaml(data=text)

        return self._call_api(
            self.client.v1.create_namespaced_service,
            namespace=namespace_name,
            body=service
        )

    def create_webserver(self, cluster, image_name):

        namespace_name = f'aaas-{cluster.name}'

        params = {
            'image': f'{settings.DOCKER_REGISTRY_FOR_K8S}{image_name}',
        }

        with compile_template('airflow_ui_deployment.yaml', cluster_id=cluster.id, **params) as text:
            deployment = load_yaml(data=text)

        self._call_api(self.client.v1beta.create_namespaced_deployment, body=deployment, namespace=namespace_name)

        with compile_template('airflow_ui_service.yaml', cluster_id=cluster.id, **params) as text:
            service = load_yaml(data=text)

        return self._call_api(
            self.client.v1.create_namespaced_service,
            namespace=namespace_name,
            body=service
        )

    def create_airflow_entity(self, cluster, entity_name, image_name, requires_service=False):
        namespace_name = f'aaas-{cluster.name}'

        params = {
            'image': f'{settings.DOCKER_REGISTRY_FOR_K8S}{image_name}',
        }

        with compile_template(f'airflow_{entity_name}_deployment.yaml', cluster_id=cluster.id, **params) as text:
            deployment = load_yaml(data=text)

        result = self._call_api(
            self.client.v1beta.create_namespaced_deployment,
            body=deployment,
            namespace=namespace_name
        )

        if requires_service:
            with compile_template(f'airflow_{entity_name}_service.yaml', cluster_id=cluster.id) as text:
                service = load_yaml(data=text)

            result = self._call_api(
                self.client.v1.create_namespaced_service,
                namespace=namespace_name,
                body=service
            )

        return result

    def update(self, cluster, entity_name, image_name):
        """
        deployment being a Deployment object...from a GET?
        """
        namespace = f'aaas-{cluster.name}'
        name = f'airflow-{entity_name}-deployment'

        deployment = self._call_api(
            self.client.v1beta.read_namespaced_deployment,
            name=name,
            namespace=namespace,
            exact=True,
            export=True
        )

        # Update container image
        deployment.spec.template.spec.containers[0].image = f'{settings.DOCKER_REGISTRY_FOR_K8S}{image_name}'
        # Update the deployment
        return self._call_api(
            self.client.v1beta.patch_namespaced_deployment,
            name=name,
            namespace=namespace,
            body=deployment
        )

    def get_secret(self, cluster):
        namespace_name = f'aaas-{cluster.name}'
        return self._call_api(
            self.client.v1.read_namespaced_secret,
            name=f'metadb-{cluster.id}',
            namespace=namespace_name
        )

    def _create_config_map(self, name, data):
        config_map = kubernetes.client.V1ConfigMap()
        config_map.metadata = kubernetes.client.V1ObjectMeta(name=name)
        config_map.data = data
        return config_map

    def _create_secret(self, name, data):
        sec = kubernetes.client.V1Secret()
        sec.metadata = kubernetes.client.V1ObjectMeta(name=name)
        sec.type = "Opaque"
        sec.data = data
        return sec

    def _call_api(self, client_func, *args, **kwargs):
        try:
            return client_func(*args, **kwargs)
        except ApiException as e:
            print(f"Exception when calling {client_func.__self__.__class__.__name__}->{client_func.__name__}: {e}\n")
            if self._raise_on_error:
                raise
