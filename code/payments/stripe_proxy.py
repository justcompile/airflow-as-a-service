import stripe as st
from django.conf import settings


class StripeProxy(object):
    def __init__(self):
        st.api_key = settings.STRIPE_SECRET_KEY

    def __getattr__(self, item):
        return getattr(st, item)