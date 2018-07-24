from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from payments.models import Product, Plan

from .stripe_proxy import StripeProxy


@receiver(pre_save, sender=Product)
def create_stripe_product(sender, instance, **kwargs):
    try:
        Product.objects.get(pk=instance.pk)
        creating = False
    except Product.DoesNotExist:
        creating = True

    if creating:
        product = StripeProxy().Product.create(
            name=instance.name,
            type='service',
        )
        instance.stripe_id = product.id


@receiver(pre_delete, sender=Product)
def delete_stripe_product(sender, instance, **kwargs):
    product = StripeProxy().Product.retrieve(instance.stripe_id)
    product.delete()


@receiver(pre_save, sender=Plan)
def create_stripe_plan(sender, instance, **kwargs):
    try:
        Plan.objects.get(pk=instance.pk)
        creating = False
    except Plan.DoesNotExist:
        creating = True

    if not creating:
        plan = StripeProxy().Plan.retrieve(instance.stripe_id)
        # we cannot change intervals, currency or amounts. If they have been, we need to delete & recreate
        # TODO: Possibly re-assign customers too
        if plan.interval != instance.interval or plan.currency != instance.currency or plan.amount != instance.amount:
            plan.delete()
            creating = True

    if creating:
        plan = StripeProxy().Plan.create(
            product=instance.product.stripe_id,
            nickname=instance.name,
            interval=instance.interval,
            currency=instance.currency,
            amount=instance.amount
        )
        instance.stripe_id = plan.id


@receiver(pre_delete, sender=Product)
def delete_stripe_plan(sender, instance, **kwargs):
    plan = StripeProxy().Plan.retrieve(instance.stripe_id)
    plan.delete()
