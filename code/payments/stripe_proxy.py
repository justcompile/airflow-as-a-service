import stripe as st
from stripe import error as errors
from django.conf import settings


class StripeProxy(object):
    errors = errors

    def __init__(self):
        st.api_key = settings.STRIPE_SECRET_KEY

    def __getattr__(self, item):
        return getattr(st, item)
