from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import ClusterEvent


class WebhookView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        return Response(request.data)

    def post(self, request, format=None):
        print(request.data)
        """
        {
            'cluster_id': 'f5eee4dd-37bd-412c-ad77-4df26af80be5', 
            'data': {'annotation.kubernetes.io/config.seen': '2018-05-15T20:54:29.63730925Z', 'annotation.kubernetes.io/config.source': 'api', 'app': 'nginx', 'image': 'k8s.gcr.io/pause-amd64:3.1', 'io.kubernetes.container.name': 'POD', 'io.kubernetes.docker.type': 'podsandbox', 'io.kubernetes.pod.name': 'nginx-deployment-59dc9fcf64-dswgg', 'io.kubernetes.pod.namespace': 'aaas-dazzling-babbage', 'io.kubernetes.pod.uid': '2945941d-5882-11e8-91cd-0800271c4eec', 'it.justcompile.aaas.cluster_id': 'f5eee4dd-37bd-412c-ad77-4df26af80be5', 'name': 'k8s_POD_nginx-deployment-59dc9fcf64-dswgg_aaas-dazzling-babbage_2945941d-5882-11e8-91cd-0800271c4eec_0', 'pod-template-hash': '1587597920', 'role': 'auth-proxy'}, 
            'description': 'Started auth-proxy', 
            'event_type': 'POD_START'
            }
        """
        try: 
            ClusterEvent.objects.create(**request.data)
        except IntegrityError:
            pass

        return Response(request.data)
