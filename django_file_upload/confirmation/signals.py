from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BuyerWiseCon, BuyerWiseTotal


@receiver(post_save, sender=BuyerWiseCon)
def buyer_wise_calc(sender, instance, **kwargs):
    # calculate total of the month for all the buyers
    total_value = sender.month_total(unit=instance.unit, session=instance.session, year=instance.year)

    defaults = {
        "buyer": instance.buyer,
        "unit": instance.unit,
        "session": instance.session,
        "year": instance.year
    }

    # create total for each month of the individual buyer
    BuyerWiseTotal.objects.update_or_create(total=total_value, session=instance.session,
                                            year=instance.year, defaults=defaults)
