import os

from django.conf import settings
import kubernetes.client
from kubernetes.client.rest import ApiException

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class K8sService(object):
    def __init__(self, config_file_path=None):
        self._config_path = config_file_path or os.path.join(settings.BASE_DIR, '.env')
        self._configuration = None
        self._client = None
        self._raise_on_error = settings.K8S['raise_on_error']

    @property
    def client(self):
        if not self._client:
            self._client = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))

        return self._client

    @property
    def configuration(self):
        if not self._configuration:
            conf_from_env = self._load_config()
            configuration = kubernetes.client.Configuration()
            configuration.api_key['authorization'] = conf_from_env['token']
            configuration.api_key_prefix['authorization'] = 'Bearer'
            configuration.host = conf_from_env['server']
            configuration.verify_ssl = False
            self._configuration = configuration

        return self._configuration

    def create_namespace(self, name):
        meta = kubernetes.client.V1ObjectMeta(
            name=f'aaas-{name}',
            labels=dict(aaas='true')
        )

        body = kubernetes.client.V1Namespace(kind='Namespace', metadata=meta)
        return self._call_api('create_namespace', body)

    def delete_namespace(self, name):
        namespace_name = f'aaas-{name}'

        body = kubernetes.client.V1DeleteOptions(
            grace_period_seconds=0,
            propagation_policy='Background'
        )

        return self._call_api('delete_namespace', namespace_name, body)

    def _call_api(self, client_func, *args):
        try:
            return getattr(self.client, client_func)(*args)
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->{client_func}: {e}\n")
            if self._raise_on_error:
                raise

    def _load_config(self):
        print(self._config_path)
        with open(self._config_path) as fp:
            return load(fp, Loader=Loader)
