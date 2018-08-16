from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Cluster, ClusterEvent
from core import tasks

from api.serializers import ClusterSerializer, ClusterEventSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        tasks.init_cluster.delay(serializer.data['id'])

    def perform_destroy(self, instance):
        tasks.delete_auth_proxy.delay(instance.name)
        super().perform_destroy(instance)

    def get_queryset(self):
        return Cluster.objects.filter(owner=self.request.user)

    @action(detail=True, url_path='events', url_name='events')
    def events(self, request, pk=None):
        serializer = ClusterEventSerializer(
            ClusterEvent.objects.filter(cluster_id=pk)[:5],
            many=True,
            context=self.get_serializer_context(),
        )

        return Response(serializer.data)
