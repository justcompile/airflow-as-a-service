from rest_framework import viewsets

from api.serializers import RepositorySerializer
from core.models import Repository


class RepositoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Repositories.
    """
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
