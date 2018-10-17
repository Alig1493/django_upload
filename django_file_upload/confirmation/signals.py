from django.db.models.signals import pre_save
from django.dispatch import receiver

from django_file_upload.core.utils import calc_sum
from .models import BuyerWise


@receiver(pre_save, sender=BuyerWise)
def buyer_wise_calc(sender, instance, **kwargs):
    instance.total = calc_sum(instance.hnm,
                              instance.esprit,
                              instance.mns,
                              instance.sainsbury,
                              instance.inditex_indirect,
                              instance.inditex_direct,
                              instance.tom_tailor,
                              instance.george,
                              instance.other,
                              instance.best_seller,
                              instance.varner,
                              instance.bestty_barclay,
                              instance.carhartt,
                              instance.bonita,
                              instance.bench)
