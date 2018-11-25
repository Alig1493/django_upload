from django.db.models import Sum

from django_file_upload.core.config import UnitType, Session


def calc_total(model, buyer, month, year):
    total = (model.objects.filter(buyer=buyer, session=month, year=year,
                                  unit__in=[UnitType.AUTO, UnitType.SEMI])
                          .aggregate(buyer_total=Sum("confirmed")))

    defaults = {
        "session": month,
        "year": year,
        "buyer": buyer,
        "unit": UnitType.TOTAL
    }

    model.objects.update_or_create(confirmed=total["buyer_total"], defaults=defaults)

    # invoke quarter and half yearly totals for each buyer
    defaults = {
        "buyer": buyer,
        "unit": UnitType.TOTAL,
        "year": year
    }
    q1_buyer_total = (model.objects.filter(unit=UnitType.TOTAL, buyer=buyer,
                                           session__in=list(range(1, Session.MAR + 1)), year=year)
                      .aggregate(buyer_total=Sum("confirmed")))
    model.objects.update_or_create(session=Session.Q1, confirmed=q1_buyer_total["buyer_total"], defaults=defaults)

    q2_buyer_total = (model.objects.filter(unit=UnitType.TOTAL, buyer=buyer,
                                           session__in=list(range(Session.APR, Session.JUN + 1)), year=year)
                      .aggregate(buyer_total=Sum("confirmed")))
    model.objects.update_or_create(session=Session.Q2, confirmed=q2_buyer_total["buyer_total"], defaults=defaults)

    model.objects.update_or_create(session=Session.H1,
                                   confirmation=q1_buyer_total["buyer_total"] + q2_buyer_total["buyer_total"],
                                   defaults=defaults)

    q3_buyer_total = (model.objects.filter(unit=UnitType.TOTAL, buyer=buyer,
                                           session__in=list(range(Session.JUL, Session.SEP + 1)), year=year)
                      .aggregate(buyer_total=Sum("confirmed")))
    model.objects.update_or_create(session=Session.Q3, confirmed=q3_buyer_total["buyer_total"], defaults=defaults)

    q4_buyer_total = (model.objects.filter(unit=UnitType.TOTAL, buyer=buyer,
                                           session__in=list(range(Session.OCT, Session.DEC + 1)), year=year)
                      .aggregate(buyer_total=Sum("confirmed")))
    model.objects.update_or_create(session=Session.Q4, confirmed=q4_buyer_total["buyer_total"], defaults=defaults)

    model.objects.update_or_create(session=Session.H2,
                                   confirmed=q3_buyer_total["buyer_total"] + q4_buyer_total["buyer_total"],
                                   defaults=defaults)
