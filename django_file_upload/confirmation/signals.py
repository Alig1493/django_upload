from django.db.models.signals import post_save
from django.dispatch import receiver

from django_file_upload.confirmation.utils import buyer_chain_reaction
from .models import BuyerWiseCon


@receiver(post_save, sender=BuyerWiseCon)
def buyer_wise_calc(sender, instance, **kwargs):

    if instance.session <= 12:
        buyer_chain_reaction(model=sender, month=instance.session,
                             year=instance.year, unit=instance.unit,
                             buyer=instance.buyer)
