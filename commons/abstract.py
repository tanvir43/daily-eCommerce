from django.db import models


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=True, null=True, blank=True)
    # updated_by = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
