from rest_framework import serializers
from core.models import ClusterEvent


class ClusterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterEvent
        fields = '__all__'
