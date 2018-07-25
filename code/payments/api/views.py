import json
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from payments.stripe_proxy import StripeProxy
from payments.models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


# def plans(request):
#     return render(request, 'payments/plans.html', {'plans': Plan.objects.all()})

# class Subscription(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = Subscription.objects.all()

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)

@require_POST
def subscribe(request):
    data = json.loads(request.body)

    token = data['token']['id']
    plan = get_object_or_404(Plan, pk=data['plan']['id'])
    stripe = StripeProxy()

    customer = stripe.Customer.create(
        email=request.user.email,
        source=token
    )

    stripe_subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{'plan': plan.stripe_id}],
    )

    subscription = Subscription.objects.create(
        stripe_id=stripe_subscription.id,
        customer_id=customer.id,
        plan=plan,
        user=request.user
    )

    return JsonResponse({'message': 'ok'})
