from rest_framework import mixins
from rest_framework import viewsets

from api.serializers import DatabaseTypeSerializer
from core.models import DatabaseType


class DBTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = DatabaseType.objects.all()
    serializer_class = DatabaseTypeSerializer
