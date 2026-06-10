from django.db import models
from django.db.models import Max


class DisplayIDMixin(models.Model):
    """
    Provides sequential display numbers and formatted public IDs
    (e.g. TKT-0001, DEV-0001) for models.
    """

    display_number = models.PositiveIntegerField(
        unique=True,
        editable=False,
        null=True,
    )

    display_prefix = None

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.display_prefix is None:
            raise ValueError("display_prefix must be set on the model.")

        if self.display_number is None:
            max_number = (
                self.__class__.objects.aggregate(max_number=Max("display_number"))[
                    "max_number"
                ]
                or 0
            )
            self.display_number = max_number + 1

        super().save(*args, **kwargs)

    @property
    def display_id(self):
        return f"{self.display_prefix}-{self.display_number:05d}"
