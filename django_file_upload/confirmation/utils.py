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
    queryset = (model.objects.filter(year=year, unit=unit,
                                     session__in=(
                                         Session.get_session_quarter(session=month)
                                         if session_length == 3 else
                                         Session.get_session_half(session=month)
                                     ),
                                     buyer=buyer)
                             .order_by('session', 'created_at')
                             .distinct("session"))

    session_total = queryset_sum(queryset=queryset)
    # print("Queryset: ", queryset)

    session_base_number = Session.Q1 - 1 if session_length == 3 else Session.H1 - 1
    # print("session month: ", month)
    # print("session length: ", session_length)
    # print("session_months_list: ", session_months_list)
    # print("session_list: ", Session.get_session_quarter(session=month))
    # print("session base: ", session_base_number, " session division: ",  session_division)
    defaults = {
        "year": year,
        "unit": unit,
        "session": session_base_number + session_division,
        "buyer": buyer
    }
    # print(defaults)
    # print(model.objects.filter(**defaults))
    # print(model.objects.filter(**defaults).count())
    # print("Session total value:", session_total)

    obj = model.objects.filter(**defaults)
    session_obj = None

    if defaults["session"] <= 18:
        if not obj.count():
            # print("Nothing exists. Creating new entry for ", defaults)
            session_obj = model.objects.create(confirmed=session_total, **defaults)
        else:
            session_obj = obj.update(confirmed=session_total)
    return session_obj


def buyer_calc_monthly_total(model, month, year, buyer):
    queryset = (model.objects.filter(buyer=buyer, session=month,
                                     year=year, unit__in=[UnitType.AUTO, UnitType.SEMI])
                             .order_by('unit', 'created_at')
                             .distinct("unit"))
    monthly_total = queryset_sum(queryset=queryset)
    # print("Queryset: ", queryset)

    defaults = {
        "year": year,
        "unit": UnitType.TOTAL,
        "session": month,
        "buyer": buyer
    }
    # print("session: ", month)
    #
    # print(defaults)
    # print(model.objects.filter(**defaults))
    # print(model.objects.filter(**defaults).count())
    # print("Monthly total value:", monthly_total)

    obj = model.objects.filter(**defaults)
    if not obj.count():
        # print("Nothing exists. Creating new entry for ", defaults)
        return model.objects.create(confirmed=monthly_total, **defaults)
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
