from django.conf.urls import url

from api.views.github_proxy import GithubProxy

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^github', GithubProxy.as_view()),
]
