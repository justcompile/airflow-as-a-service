from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import Build, BuildLog, Cluster
from api.serializers import BuildSerializer, ClusterSerializer


@receiver(pre_save, sender=Build)
def send_build_status_to_channel(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    user_id = instance.repository.owner_id

    try:
        Build.objects.get(pk=instance.pk)
        action = 'UPDATE'
    except Build.DoesNotExist:
        action = 'CREATE'

    async_to_sync(channel_layer.group_send)(
        f'builds-{str(user_id)}', {
            "type": "build.message",
            "message": {
                'action': action,
                'data': BuildSerializer(instance).data,
            },
        },
    )


@receiver(pre_save, sender=BuildLog)
def send_build_log_to_channel(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    user_id = instance.repository.owner_id

    try:
        Build.objects.get(pk=instance.pk)
        action = 'UPDATE'
    except Build.DoesNotExist:
        action = 'CREATE'

    async_to_sync(channel_layer.group_send)(
        f'builds-{str(user_id)}', {
            "type": "build.message",
            "message": {
                'action': action,
                'data': BuildSerializer(instance).data,
            },
        },
    )


@receiver(pre_save, sender=Cluster)
def send_cluster_status_to_channel(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    user_id = instance.owner_id

    async_to_sync(channel_layer.group_send)(
        f'clusters-{str(user_id)}', {
            "type": "cluster.message",
            "message": {
                'action': 'UPDATE',
                'data': ClusterSerializer(instance).data,
            },
        },
    )
