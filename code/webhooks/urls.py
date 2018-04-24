from django.conf.urls import url

from webhooks.views import WebhookView

urlpatterns = [
    url(r'^event', WebhookView.as_view()),
]
