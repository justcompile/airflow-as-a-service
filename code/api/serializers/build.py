from rest_framework import serializers
from core.models import (
    Build,
)


class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = '__all__'
