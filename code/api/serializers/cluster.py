from rest_framework import serializers
from core.models import (
    Cluster,
    DatabaseInstance,
    DatabaseType,
)

from .dbs import DatabaseInstanceSerializer


class ClusterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    db_instance = DatabaseInstanceSerializer(read_only=True)

    class Meta:
        model = Cluster
        fields = '__all__'

    def create(self, validated_data):
        db_type = DatabaseType.objects.get(pk=self.initial_data['dbType'])
        db_instance = DatabaseInstance.objects.create(db_type=db_type)

        validated_data['db_instance_id'] = db_instance.id
        instance = super().create(validated_data)

        return instance
