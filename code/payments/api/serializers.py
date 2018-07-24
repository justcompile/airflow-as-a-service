from rest_framework import serializers
from payments.models import (
    Plan,
    Feature,
    PlanFeature,
)


# class PlanFeatureSerializer(serializers.ModelSerializer):
#     name = serializers.ReadOnlyField()
#     key = serializers.ReadOnlyField()
#     value = serializers.ReadOnlyField(source='plan_feature.value')

#     class Meta:
#         model = Feature
#         fields = ('name', 'key', 'value',)
class PlanFeatureSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='feature.name')
    key = serializers.ReadOnlyField(source='feature.key')
    value = serializers.ReadOnlyField()

    class Meta:
        model = PlanFeature
        fields = ('name', 'key', 'value',)


class PlanSerializer(serializers.ModelSerializer):
    features = PlanFeatureSerializer(source='planfeature_set', many=True)
    class Meta:
        model = Plan
        exclude = ('stripe_id',)
