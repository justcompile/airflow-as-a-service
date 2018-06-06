from rest_framework import serializers
from core.models import (
    DatabaseInstance,
    DatabaseType,
)


class DatabaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseType
        fields = '__all__'


class DatabaseInstanceSerializer(serializers.ModelSerializer):
    varient = serializers.CharField(source='db_type.varient')
    version = serializers.CharField(source='db_type.version')

    class Meta:
        model = DatabaseInstance
        fields = [
            'varient',
            'version',
            'created_at',
        ]
