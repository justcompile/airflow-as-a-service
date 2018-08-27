from rest_framework import serializers
from core.models import (
    BuildLog,
)


class BuildLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildLog
        fields = ['lines']
