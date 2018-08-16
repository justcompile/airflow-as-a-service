from rest_framework import serializers
from payments.models import (
    Plan,
    PlanFeature,
    Subscription,
)


class PlanFeatureSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='feature.name')
    key = serializers.ReadOnlyField(source='feature.key')
    value = serializers.ReadOnlyField()

    class Meta:
        model = PlanFeature
        fields = ('name', 'key', 'value')


class PlanSerializer(serializers.ModelSerializer):
    features = PlanFeatureSerializer(source='planfeature_set', many=True)
    subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Plan
        exclude = ('stripe_id',)

    def get_subscribed(self, obj):
        try:
            user_subscription = self.context['request'].user.subscription
            return user_subscription.id and obj.id == user_subscription.plan_id
        except Subscription.DoesNotExist:
            return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
