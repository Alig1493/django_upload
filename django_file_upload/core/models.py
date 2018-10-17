from django.db import models

from django_file_upload.core.config import Session, UnitType


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class UnitSessionTimeStampModel(TimeStampModel):
    unit = models.IntegerField(choices=UnitType.CHOICES)
    session = models.IntegerField(choices=Session.CHOICES)
    year = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True
