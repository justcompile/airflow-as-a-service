from rest_framework import viewsets
from core.models import Cluster
from core.services.kube import K8sService

from api.serializers import ClusterSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.k8s = K8sService()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.k8s.create_namespace(serializer.data['name'])

    def perform_destroy(self, instance):
        self.k8s.delete_namespace(instance.name)
        super().perform_destroy(instance)

    def get_queryset(self):
        return Cluster.objects.filter(owner=self.request.user)
