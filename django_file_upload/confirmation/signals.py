from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_file_upload.core.config import Session
from .models import BuyerWiseCon, BuyerWiseTotal


@receiver(post_save, sender=BuyerWiseCon)
def buyer_wise_calc(sender, instance, **kwargs):
    # calculate total of the month for the buyer
    total_value = (sender.objects.filter(unit=instance.unit,
                                         session=instance.session, year=instance.year)
                                 .aggregate(buyer_total=Sum("confirmed")))

    defaults = {
        "buyer": instance.buyer,
        "unit": instance.unit,
        "session": instance.session,
        "year": instance.year
    }

    # create total for each month
    BuyerWiseTotal.objects.update_or_create(total=total_value["buyer_total"], defaults=defaults)

    # invoke quarter and half yearly totals for each buyer
    defaults = {
        "buyer": instance.buyer,
        "unit": instance.unit,
        "year": instance.year
    }
    print(defaults)
    q1_buyer_total = (BuyerWiseCon.objects.filter(unit=instance.unit, buyer=instance.buyer,
                                                  session__in=list(range(1, Session.MAR + 1)), year=instance.year)
                      .aggregate(buyer_total=Sum("confirmed")))
    print(q1_buyer_total)
    print(BuyerWiseCon.objects.filter(**defaults))
    obj, created = BuyerWiseCon.objects.update_or_create(session=Session.Q1, confirmed=q1_buyer_total["buyer_total"],
                                          defaults=defaults)
    print(obj)
    print(created)
    #
    # q2_buyer_total = (BuyerWiseCon.objects.filter(unit=instance.unit, buyer=instance.buyer,
    #                                               session__in=list(range(Session.APR, Session.JUN + 1)),
    #                                               year=instance.year)
    #                   .aggregate(buyer_total=Sum("confirmed")))
    # BuyerWiseCon.objects.update_or_create(session=Session.Q2, confirmed=q2_buyer_total["buyer_total"],
    #                                       defaults=defaults)
    #
    # BuyerWiseCon.objects.update_or_create(session=Session.H1,
    #                                       confirmed=q1_buyer_total["buyer_total"] + q2_buyer_total["buyer_total"],
    #                                       defaults=defaults)
    #
    # q3_buyer_total = (BuyerWiseCon.objects.filter(unit=instance.unit, buyer=instance.buyer,
    #                                               session__in=list(range(Session.JUL, Session.SEP + 1)),
    #                                               year=instance.year)
    #                   .aggregate(buyer_total=Sum("confirmed")))
    # BuyerWiseCon.objects.update_or_create(session=Session.Q3, confirmed=q3_buyer_total["buyer_total"],
    #                                       defaults=defaults)
    #
    # q4_buyer_total = (BuyerWiseCon.objects.filter(unit=instance.unit, buyer=instance.buyer,
    #                                               session__in=list(range(Session.OCT, Session.DEC + 1)),
    #                                               year=instance.year)
    #                   .aggregate(buyer_total=Sum("confirmed")))
    # BuyerWiseCon.objects.update_or_create(session=Session.Q4, confirmed=q4_buyer_total["buyer_total"],
    #                                       defaults=defaults)
    #
    # BuyerWiseCon.objects.update_or_create(session=Session.H2,
    #                                       confirmed=q3_buyer_total["buyer_total"] + q4_buyer_total["buyer_total"],
    #                                       defaults=defaults)
    #
    # calc_total(BuyerWiseCon, instance.buyer, instance.session, instance.year)
