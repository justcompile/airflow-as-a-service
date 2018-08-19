import unittest
from unittest import mock

from django_test_utils.signals import disconnect_signals

from payments.models import Product, Plan
from payments import signals


class PaymentSignalsTestCase(unittest.TestCase):
    def setUp(self):
        stripe_patcher = mock.patch('payments.signals.StripeProxy')
        self.stripe = stripe_patcher.start()
        self.addCleanup(stripe_patcher.stop)

        disconnect_signals(signals)

    def tearDown(self):
        Plan.objects.all().delete()
        Product.objects.all().delete()

    def test_create_stripe_product_doesnt_call_stripe_if_product_already_exists(self):
        prod = Product.objects.create(name='My Product', stripe_id='stripe-123')

        signals.create_stripe_product(None, prod)
        self.stripe.assert_not_called()

    def test_create_stripe_product_does_call_stripe_if_product_is_new(self):
        prod = Product(name='My Product')
        self.stripe().Product.create.return_value = mock.Mock(id='stripe-456')

        signals.create_stripe_product(None, prod)
        self.stripe().Product.create.assert_called_with(
            name='My Product',
            type='service',
        )

        self.assertEqual(prod.stripe_id, 'stripe-456')

    def test_delete_stripe_product(self):
        prod = Product(name='My Product', stripe_id='12345')

        stripe_product = mock.Mock()

        self.stripe().Product.retrieve.return_value = stripe_product
        signals.delete_stripe_product(None, prod)

        stripe_product.delete.assert_called_with()

    def test_create_stripe_plan_simply_creates_it_if_does_not_already_exist(self):
        prod = Product(name='My Product', stripe_id='12345')
        plan = Plan(
            name='My Plan',
            currency='gbp',
            amount=1000,
            interval='monthly',
            product=prod,
        )

        signals.create_stripe_plan(None, plan)

        self.stripe().Plan.retrieve.assert_not_called()
        self.stripe().Plan.create.assert_called_with(
            product=prod.stripe_id,
            nickname=plan.name,
            interval=plan.interval,
            currency=plan.currency,
            amount=plan.amount,
        )

    def test_create_stripe_plan_deletes_existing_before_creating_new_plan(self):
        prod = Product.objects.create(name='My Product', stripe_id='12345')
        plan = Plan.objects.create(
            name='My Plan',
            currency='gbp',
            amount=1000,
            interval='monthly',
            product=prod,
            stripe_id='stripe-plan-12345',
        )

        stripe_plan = mock.Mock()
        self.stripe().Plan.retrieve.return_value = stripe_plan

        signals.create_stripe_plan(None, plan)

        stripe_plan.delete.assert_called_with()
        self.stripe().Plan.retrieve.assert_called_with('stripe-plan-12345')
        self.stripe().Plan.create.assert_called_with(
            product=prod.stripe_id,
            nickname=plan.name,
            interval=plan.interval,
            currency=plan.currency,
            amount=plan.amount,
        )

    def test_create_stripe_plan_doesnt_delete_and_update_plan_if_nothing_changed(self):
        prod = Product.objects.create(name='My Product', stripe_id='12345')
        plan = Plan.objects.create(
            name='My Plan',
            currency='gbp',
            amount=1000,
            interval='monthly',
            product=prod,
            stripe_id='stripe-plan-12345',
        )

        stripe_plan = mock.Mock(
            interval=plan.interval,
            currency=plan.currency,
            amount=plan.amount,
        )

        self.stripe().Plan.retrieve.return_value = stripe_plan

        signals.create_stripe_plan(None, plan)

        stripe_plan.delete.assert_not_called()
        self.stripe().Plan.retrieve.assert_called_with('stripe-plan-12345')
        self.stripe().Plan.create.assert_not_called()

    def test_delete_stripe_plan(self):
        plan = Plan(name='My Plan', stripe_id='12345')

        stripe_plan = mock.Mock()

        self.stripe().Plan.retrieve.return_value = stripe_plan
        signals.delete_stripe_plan(None, plan)

        stripe_plan.delete.assert_called_with()
