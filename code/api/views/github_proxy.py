from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.views import APIView
from rest_framework.response import Response

from github import Github


class GithubProxy(APIView):
    """
    View to return all Github repos which the authenticated user has access to
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        social = request.user.social_auth.get(provider='github')
        g = Github(social.extra_data['access_token'])
        return Response([
            {'name': repo.name, 'private': repo.private, 'url': repo.html_url} 
            for repo in g.get_user().get_repos(type='all')
        ])

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
