from django.conf import settings
from django.db.utils import IntegrityError
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import (
    ClusterEvent,
    Repository,
    Build,
)
from core.services.git import GitClient
from core.tasks import process_git_push

from payments.stripe_proxy import StripeProxy


class WebhookView(APIView):
    authentication_classes = ()
    permission_classes = ()


class GithubPushView(WebhookView):
    def post(self, request, format=None):
        if 'head_commit' not in request.data:
            raise ParseError('Incorrect payload format received')

        parsed_commit = GitClient.parse_webhook_message(request.data)

        for repo in Repository.objects.filter(url=parsed_commit['repo_url']):
            for cluster in repo.clusters.values('id'):
                build = Build.objects.create(
                    branch=parsed_commit["branch"],
                    committer=parsed_commit["committer"],
                    commit_id=parsed_commit["commit_id"],
                    message=parsed_commit["message"],
                    repository=repo,
                    status=Build.QUEUED,
                )

                process_git_push.delay(build.id, cluster['id'])

        return Response({'message': 'ok'})


class K8sEventView(WebhookView):
    def post(self, request, format=None):
        try:
            ClusterEvent.objects.create(**request.data)
        except IntegrityError:
            pass

        return Response(request.data)


class StripeEventView(WebhookView):
    def post(self, request, format=None):
        payload = request.data
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        stripe = StripeProxy()

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOKS_SECRET
            )
        except ValueError:
            # Invalid payload
            return Response(status=400)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return Response(status=400)

        # Do something with event

        return Response(status=200)
