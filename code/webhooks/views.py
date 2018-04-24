from rest_framework.views import APIView
from rest_framework.response import Response


class WebhookView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        return Response(request.data)

    def post(self, request, format=None):
        return Response(request.data)
