from rest_framework import viewsets

from core.models import Build

from api.permissions import IsOwnerOrReadOnly
from api.serializers import BuildSerializer


class BuildViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return Build.objects.filter(repository__owner_id=self.request.user.id)
