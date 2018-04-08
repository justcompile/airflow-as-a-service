from rest_framework import viewsets
from core.models import Cluster

from api.serializers import ClusterSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

    def get_queryset(self):
        return Cluster.objects.filter(owner=self.request.user)
