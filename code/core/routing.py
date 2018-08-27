from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/builds/$', consumers.BuildConsumer),
    url(r'^ws/build/()/log/$', consumers.BuildItemsConsumer),
    url(r'^ws/clusters/$', consumers.ClusterConsumer),
]
