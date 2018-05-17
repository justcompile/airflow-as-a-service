from rest_framework import serializers
from core.models import DatabaseType


class DatabaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseType
        fields = '__all__'
