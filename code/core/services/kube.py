import os

from django.conf import settings
import kubernetes.client
from kubernetes.client.rest import ApiException

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from core.utils.htpasswd import HTPasswd


class K8sClient(object):
    def __init__(self, config_file_path=None):
        self._config_path = config_file_path or os.path.join(settings.BASE_DIR, '.env')
        self._config = None
        self._clients = {}

        self.__version_map = {
            'v1': kubernetes.client.CoreV1Api,
            'v1beta': kubernetes.client.ExtensionsV1beta1Api,
        }

    @property
    def config(self):
        if not self._config:
            conf_from_env = self._load_config()
            configuration = kubernetes.client.Configuration()
            configuration.api_key['authorization'] = conf_from_env['token']
            configuration.api_key_prefix['authorization'] = 'Bearer'
            configuration.host = conf_from_env['server']
            configuration.verify_ssl = False
            self._config = configuration

        return self._config

    def _load_config(self):
        print(self._config_path)
        with open(self._config_path) as fp:
            return load(fp, Loader=Loader)

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
        with open(file_path) as fp:
            dep = load(fp, Loader=Loader)

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

    def create_auth_proxy(self, name, username=None, password=None):
        assert username and password, 'Must specify username and password'

        namespace_name = f'aaas-{name}'
        self._call_api(self.client.v1.create_namespaced_config_map, namespace=namespace_name, body=self._create_config_map())
        self._call_api(
            self.client.v1.create_namespaced_secret,
            namespace=namespace_name,
            body=self._create_secret(username, password)
        )

        with open(os.path.join(settings.BASE_DIR, 'k8s_files/proxy_deployment.yaml')) as fp:
            deployment = load(fp, Loader=Loader)

        self._call_api(self.client.v1beta.create_namespaced_deployment, body=deployment, namespace=namespace_name)

        with open(os.path.join(settings.BASE_DIR, 'k8s_files/proxy_service.yaml')) as fp:
            service = load(fp, Loader=Loader)

        return self._call_api(
            self.client.v1.create_namespaced_service,
            namespace=namespace_name,
            body=service
        )

    def _create_config_map(self):
        config_map = kubernetes.client.V1ConfigMap()
        config_map.metadata = kubernetes.client.V1ObjectMeta(name="proxy-auth-template")
        with open(os.path.join(settings.BASE_DIR, 'k8s_files/proxy_auth.template')) as fp:
            config_map.data = {"proxy_auth.template": fp.read()}
        return config_map

    def _create_secret(self, username, password):
        sec = kubernetes.client.V1Secret()
        sec.metadata = kubernetes.client.V1ObjectMeta(name="proxy-htpasswd-secret")
        sec.type = "Opaque"
        sec.data = {".htpasswd": HTPasswd.generate(username, password, encode=True)}
        return sec

    def _call_api(self, client_func, *args, **kwargs):
        try:
            return client_func(*args, **kwargs)
        except ApiException as e:
            print(f"Exception when calling {client_func.__self__.__class__.__name__}->{client_func.__name__}: {e}\n")
            if self._raise_on_error:
                raise
