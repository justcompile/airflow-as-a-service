from rest_framework import serializers
from core.models import (
    Cluster,
    DatabaseInstance,
    DatabaseType,
    Repository,
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
        repo = Repository.objects.get(pk=self.initial_data['repository'], owner=validated_data['owner'])

        db_type = DatabaseType.objects.get(pk=self.initial_data['dbType'])
        db_instance = DatabaseInstance.objects.create(db_type=db_type)

        validated_data['db_instance_id'] = db_instance.id
        validated_data['repository_id'] = repo.id

        return super().create(validated_data)
