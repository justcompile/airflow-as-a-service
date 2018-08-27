from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from core.models import Build, BuildLog

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    BuildSerializer,
    BuildLogSerializer,
)


class BuildViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    @action(detail=True, url_path='log', url_name='log')
    def log(self, request, pk=None):
        if pk is None:
            raise NotFound

        log = BuildLog.objects.get(build_id=pk)

        return Response(BuildLogSerializer(log).data)

    def get_queryset(self):
        return Build.objects.filter(repository__owner_id=self.request.user.id)
