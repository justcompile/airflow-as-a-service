from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, views
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from payments.stripe_proxy import StripeProxy, errors
from payments.models import Plan, Subscription
from .serializers import PlanSerializer


class PlanViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


# def plans(request):
#     return render(request, 'payments/plans.html', {'plans': Plan.objects.all()})

# class Subscription(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = Subscription.objects.all()

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)


class SubscribeView(views.APIView):
    def post(self, request, **kwargs):
        token = request.data['token']['id']
        plan = get_object_or_404(Plan, pk=request.data['plan']['id'])
        stripe = StripeProxy()

        try:
            customer = stripe.Customer.create(
                email=request.user.email,
                source=token,
            )

            stripe_subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{'plan': plan.stripe_id}],
            )

            Subscription.objects.create(
                stripe_id=stripe_subscription.id,
                customer_id=customer.id,
                plan=plan,
                user=request.user,
            )
        except errors.StripeError as e:
            raise ParseError(e)

        return Response(PlanSerializer(plan, context={'request': request}).data)
