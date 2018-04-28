from django.conf.urls import url

from webhooks.views import WebhookView

app_name = 'webhooks'

urlpatterns = [
    url(r'^event', WebhookView.as_view()),
]
