import uuid

from django.conf import settings
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
