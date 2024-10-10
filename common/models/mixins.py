from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class DateMixin(models.Model):
    created_at = models.DateTimeField("Created at", null=True, blank=False)
    updated_at = models.DateTimeField("Updated at", null=True, blank=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DateMixin, self).save(*args, **kwargs)
