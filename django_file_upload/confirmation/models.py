from django.db import models

from django_file_upload.core.models import UnitSessionTimeStampModel

# TODO: In addition to UnitSessionTimeStampModel fields, BuyerWise will now have only three more fields-- buyer, confirmed, total. The total needs to be calculated from backend. You'll have to update your frontend template as well to conform to these mentioned changes.
class BuyerWise(UnitSessionTimeStampModel):
    hnm = models.FloatField(blank=True, null=True, verbose_name="H&M")
    esprit = models.FloatField(blank=True, null=True, verbose_name="ESPRIT")
    mns = models.FloatField(blank=True, null=True, verbose_name="M&S")
    sainsbury = models.FloatField(blank=True, null=True, verbose_name="SAINSBURY")
    inditex_indirect = models.FloatField(blank=True, null=True, verbose_name="INDITEX- (INDIRECT)")
    inditex_direct = models.FloatField(blank=True, null=True, verbose_name="INDITEX- (DIRECT)")
    tom_tailor = models.FloatField(blank=True, null=True, verbose_name="TOM TAILOR")
    george = models.FloatField(blank=True, null=True, verbose_name="GEORGE")
    other = models.FloatField(blank=True, null=True, verbose_name="OTHER")
    best_seller = models.FloatField(blank=True, null=True, verbose_name="BEST SELLER")
    varner = models.FloatField(blank=True, null=True, verbose_name="VARNER")
    bestty_barclay = models.FloatField(blank=True, null=True, verbose_name="BESTTY BARCLAY")
    carhartt = models.FloatField(blank=True, null=True, verbose_name="CARHARTT")
    bonita = models.FloatField(blank=True, null=True, verbose_name="BONITA")
    bench = models.FloatField(blank=True, null=True, verbose_name="BENCH")
    total = models.FloatField(blank=True, null=True, )

    class Meta:
        verbose_name = "Buyer wise Confirmation (Pc)"
        verbose_name_plural = "Buyer wise Confirmation (Pcs)"

    def __str__(self):
        return f"{self.get_session_display()}/{self.year}-{self.get_unit_display()}"
