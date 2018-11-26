import math

from django.db.models import Sum

from django_file_upload.core.config import Session, UnitType
from django_file_upload.core.utils import get_session_division


def queryset_sum(queryset):

    confirmed_sum = 0

    for obj in queryset:
        confirmed_sum += obj.confirmed

    return confirmed_sum


def buyer_session_wise_calc(model, month, year, unit, buyer, session_length):
    session_division = get_session_division(month, session_length)
    session_months_list = list(range(1, session_length+1))
    session_list = [i*session_division for i in session_months_list]

    session_total = queryset_sum(queryset=model.objects.filter(year=year, unit=unit,
                                                               session__in=session_list, buyer=buyer)
                                                       .order_by('session', 'created_at')
                                                       .distinct("session"))

    session_base_number = Session.Q1 - 1 if session_length == 3 else Session.H1 - 1
    defaults = {
        "year": year,
        "unit": unit,
        "session": session_base_number + session_division,
        "buyer": buyer
    }
    print(defaults)
    print(model.objects.filter(**defaults))
    print(model.objects.filter(**defaults).count())
    obj = model.objects.filter(**defaults)
    if not obj.count():
        model.objects.create(confirmed=session_total, **defaults)
    return obj.update(confirmed=session_total)


def buyer_calc_monthly_total(model, month, year, buyer):
    monthly_total = queryset_sum(queryset=model.objects.filter(buyer=buyer, session=month,
                                                               year=year, unit__in=[UnitType.AUTO, UnitType.SEMI])
                                                       .order_by('unit', 'created_at')
                                                       .distinct("unit"))

    defaults = {
        "year": year,
        "unit": UnitType.TOTAL,
        "session": month,
        "buyer": buyer
    }

    print(defaults)
    print(model.objects.filter(**defaults))
    print(model.objects.filter(**defaults).count())

    obj = model.objects.filter(**defaults)
    if not obj.count():
        model.objects.create(confirmed=monthly_total, **defaults)
    return obj.update(confirmed=monthly_total)


def buyer_quarter_calc(model, month, year, unit, buyer):
    return buyer_session_wise_calc(model, month, year, unit, buyer, 3)


def buyer_half_calc(model, month, year, unit, buyer):
    return buyer_session_wise_calc(model, month, year, unit, buyer, 6)


def buyer_chain_reaction(model, month, year, unit, buyer):
    buyer_quarter_calc(model, month, year, unit, buyer)
    buyer_half_calc(model, month, year, unit, buyer)

    # monthly calculations
    buyer_calc_monthly_total(model, month, year, buyer)
    buyer_quarter_calc(model, month, year, 2, buyer)
    buyer_half_calc(model, month, year, 2, buyer)
