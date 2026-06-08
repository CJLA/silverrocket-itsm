from core.utils import shorten_uuid
from django.db import models


class ShortUUIDMixin(models.Model):
    """
    Provides a human-readable short identifier derived from the model UUID.
    """

    class Meta:
        abstract = True

    @property
    def display_id(self):
        return shorten_uuid(self.id)
