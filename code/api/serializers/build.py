from rest_framework import serializers
from core.models import (
    Build,
)

from .repository import RepositorySerializer


class BuildSerializer(serializers.ModelSerializer):
    repository = RepositorySerializer()

    class Meta:
        model = Build
        fields = '__all__'
