from rest_framework import serializers
from core.models import Cluster


class ClusterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Cluster
        fields = '__all__'
