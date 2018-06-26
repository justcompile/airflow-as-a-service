from django.conf.urls import url

from webhooks.views import (
    GithubPushView,
    K8sEventView,
)

app_name = 'webhooks'

urlpatterns = [
    url(r'^event', K8sEventView.as_view()),
    url(r'^git-push', GithubPushView.as_view()),
]
