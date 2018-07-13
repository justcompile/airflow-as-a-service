import uuid
from django.conf import settings
from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    stripe_id = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} ({self.stripe_id})'


class Plan(models.Model):
    interval_choices = (
        ('month', 'Monthly'),
        ('Year', 'Annually'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    amount = models.IntegerField()
    currency = models.CharField(max_length=3)
    interval = models.CharField(max_length=10, choices=interval_choices)
    stripe_id = models.CharField(max_length=200)

    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.amount/100}{self.currency} {self.interval}'


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stripe_id = models.CharField(max_length=200)
    customer_id = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
