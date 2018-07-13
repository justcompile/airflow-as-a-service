from rest_framework import mixins, viewsets

from payments.models import Plan
from .serializers import PlanSerializer


class PlanViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


# def plans(request):
#     return render(request, 'payments/plans.html', {'plans': Plan.objects.all()})


# def subscribe(request):
#     token = request.POST['token']
#     plan = get_object_or_404(Plan, pk=request.POST['plan'])
#     stripe = StripeProxy()

#     customer = stripe.Customer.create(
#         email=request.user.email,
#         source=token
#     )

#     stripe_subscription = stripe.Subscription.create(
#         customer=customer.id,
#         items=[{'plan': plan.stripe_id}],
#     )

#     subscription = Subscription(
#         stripe_id=stripe_subscription.id,
#         customer_id=customer.id,
#         plan=plan,
#         user=request.user
#     )
