from django.core.cache import cache
from django.utils.cache import learn_cache_key
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from github import Github
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers.github import GitRepo
from core.models import Repository


class FauxResponse(object):
    """
    In order to invalidate the cache, we need access to the response
    to generate the cache key.
    As such, we need a fake response object
    """
    def __init__(self, request):
        self._request = request

    def has_header(self, key):
        if key == 'Vary' and 'HTTP_ACCEPT' in self._request.META:
            return True
        return False

    def __getitem__(self, key):
        if self.has_header(key):
            return 'Accept, Cookie'


class GithubProxy(APIView):
    """
    View to return all Github repos which the authenticated user has access to
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """

        user_repos = [row[0] for row in Repository.objects.filter(owner=request.user).values_list('name')]

        social = request.user.social_auth.get(provider='github')
        g = Github(social.extra_data['access_token'])
        return Response(
            GitRepo(
                self._set_selected(user_repos, g.get_user().get_repos(type='all')),
                many=True
            ).data
        )

    def post(self, request, format=None):
        repo = request.data['repo']
        model_fields = [field.name for field in Repository._meta.get_fields()]

        payload = {
            k: v
            for k, v in repo.items()
            if k in model_fields
        }

        payload['owner'] = request.user

        _, created = Repository.objects.get_or_create(**payload)
        if not created:
            return Response({'message': 'Repo already selected'}, status=status.HTTP_409_CONFLICT)

        repo['selected'] = True

        cache_key = learn_cache_key(request, FauxResponse(request))
        cache.delete(cache_key.replace('POST', 'GET'))

        return Response(repo, status=status.HTTP_201_CREATED)

    def _set_selected(self, selected_repos, git_repos):
        for repo in git_repos:
            setattr(repo, 'selected', repo.name in selected_repos)
            yield repo

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
