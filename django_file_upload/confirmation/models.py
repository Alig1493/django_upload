from django.db import models

from django_file_upload.core.models import UnitSessionTimeStampModel


# TODO: In addition to UnitSessionTimeStampModel fields,
# BuyerWise will now have only three more fields-- buyer, confirmed, total.
# The total needs to be calculated from backend.
# You'll have to update your frontend template as well to conform to these mentioned changes.


class Buyer(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class BuyerWiseCon(UnitSessionTimeStampModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="buyerwise")
    confirmed = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Buyer wise Confirmation (Pc)"
        verbose_name_plural = "Buyer wise Confirmation (Pcs)"

    def __str__(self):
        return f"{self.get_session_display()}/{self.year}-{self.get_unit_display()}"


class BuyerWiseTotal(UnitSessionTimeStampModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="buyerwise_total")
    total = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_session_display()}/{self.year}-{self.get_unit_display()}"
