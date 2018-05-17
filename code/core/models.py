import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from core.utils.name_generator import get_random_name


class Cluster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    ui_endpoint = models.CharField(max_length=200, null=True, blank=True)
    requested_at = models.DateField(auto_now_add=True)
    created_at = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=40, default='pending')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    db_instance = models.ForeignKey(
        'DatabaseInstance',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self._state.adding and not self.name:
            self.name = get_random_name()

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )


class ClusterEvent(models.Model):
    CLUSTER_START = 'CLUSTER_START'
    CLUSTER_STOP = 'CLUSTER_STOP'
    POD_START = 'POD_START'
    POD_STOP = 'POD_STOP'

    event_types = (
        (CLUSTER_START, 'Cluster Started'),
        (CLUSTER_STOP, 'Cluster Stopped'),
        (POD_START, 'Pod Started'),
        (POD_STOP, 'Pod Stopped'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    description = models.CharField(max_length=100, null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=event_types)

    data = JSONField(null=True, blank=True)

    cluster = models.ForeignKey('Cluster', on_delete=models.CASCADE)

    class Meta:
        indexes = (
            models.Index(fields=['cluster_id', '-created_at']),
        )

        ordering = ['-created_at']


class DatabaseInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    db_type = models.ForeignKey('DatabaseType', on_delete=models.CASCADE)


class DatabaseType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    varient = models.CharField(max_length=50)
    version = models.CharField(max_length=8)
    icon = models.URLField(max_length=300)
    docker_image = models.CharField(max_length=100)

    class Meta:
        ordering = ['varient', 'version']

    def __str__(self):
        return f"{self.varient} ({self.version})"
