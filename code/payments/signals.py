from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from payments.models import Product, Plan

from .stripe_proxy import StripeProxy


@receiver(pre_save, sender=Product)
def create_stripe_product(sender, instance, **kwargs):
    if not instance.pk:
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
    if not instance.pk:
        plan = StripeProxy().Plan.create(
            product=instance.product.stripe_id,
            nickname=instance.name,
            interval=instance.interval,
            currency=instance.currency,
            amount=instance.amount
        )
        instance.stripe_id = plan.id
    else:
        plan = StripeProxy().Plan.retrieve(instance.stripe_id)
        plan.nickname = instance.name
        plan.interval = instance.interval
        plan.currency = instance.currency
        plan.amount = instance.amount
        plan.save()


@receiver(pre_delete, sender=Product)
def delete_stripe_plan(sender, instance, **kwargs):
    plan = StripeProxy().Plan.retrieve(instance.stripe_id)
    plan.delete()
