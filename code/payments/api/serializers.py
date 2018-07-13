from rest_framework import serializers
from payments.models import (
    Plan,
)


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        exclude = ('stripe_id',)
