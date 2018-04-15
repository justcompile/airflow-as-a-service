from rest_framework import viewsets
from core.models import Cluster
# from core.services.kube import K8sService
from core import tasks

from api.serializers import ClusterSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.k8s = K8sService()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        tasks.create_auth_proxy.delay(serializer.data['id'])

    def perform_destroy(self, instance):
        tasks.delete_auth_proxy.delay(instance.name)
        super().perform_destroy(instance)

    def get_queryset(self):
        return Cluster.objects.filter(owner=self.request.user)
