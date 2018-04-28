from django.conf.urls import url

from api.views.github_proxy import GithubProxy
from .router import urlpatterns as router_urls

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
app_name = 'api'

urlpatterns = [
    url(r'^github', GithubProxy.as_view()),
] + router_urls
