import math

from django.db.models import Sum

from django_file_upload.core.config import EXCLUDE_FIELDS, UnitType, Session


def calc_rate(num, denom):
    if num is None or denom is None:
        return 0
    else:
        return num * 100 / denom


def calc_sum(*args):
    summation = 0
    count = 0
    for val in args:
        if val is not None:
            count += 1
            summation += val
    if count > 0:
        return summation


def calc_diff(minuend, subtrahend):
    if minuend is not None and subtrahend is not None:
        return minuend - subtrahend
    if minuend is None and subtrahend is not None:
        return - subtrahend
    if minuend is not None and subtrahend is None:
        return minuend


def get_include_fields(model, exclude_fields=EXCLUDE_FIELDS):
    return [f.name for f in model._meta.get_fields() if f.name not in exclude_fields]


def get_session_division(month, session_length):
    # returns the session(quarter/half) number to which the month belongs to
    return int(math.ceil(month/session_length))


def session_wise_calc(model, month, year, unit, session_length):
    session_division = get_session_division(month, session_length)
    include_fields = get_include_fields(model=model)
    # print("Getting sessions for month:", month)
    # print("Sessions:", Session.get_session_quarter(session=month)
    #       if session_length == 3 else Session.get_session_half(session=month))

    ids = model.objects.filter(unit=unit, session__in=(
                                         Session.get_session_quarter(session=month)
                                         if session_length == 3 else
                                         Session.get_session_half(session=month)
                                     ), year=year).order_by('session', 'created_at').distinct('session').values_list('id', flat=True)
    aggregate_args = [Sum(x) for x in include_fields]
    fields_sum = model.objects.filter(id__in=ids).aggregate(*aggregate_args)
    session_args = {}
    for field in include_fields:
        session_args[field] = fields_sum[f"{field}__sum"]
    session_base_number = Session.Q1-1 if session_length == 3 else Session.H1-1

    # if year == 2019 and month == 7 and unit == 0:
    #     print("==============================================")
    #     print("==============================================")
    #     print("==============================================")
    #     print("==============================================")
    #     print(model)
    #     print(ids)
    #     print(session_args)
    #     print(session_base_number+session_division)
    #     print("==============================================")
    #     print("==============================================")
    #     print("==============================================")
    #     print("==============================================")

    return model.objects.update_or_create(year=year, unit=unit, session=session_base_number+session_division, defaults=session_args)


def calc_monthly_total(model, month, year,):
    ids = model.objects.filter(session=month, year=year, unit__in=[UnitType.AUTO, UnitType.SEMI]) \
        .order_by('unit', 'created_at') \
        .distinct('unit') \
        .values_list('id', flat=True)
    exclude_fields = EXCLUDE_FIELDS
    include_fields = [f.name for f in model._meta.get_fields() if f.name not in exclude_fields]
    aggregate_args = [Sum(x) for x in include_fields]
    fields_sum = model.objects.filter(id__in=ids).aggregate(*aggregate_args)
    session_args = {}
    for field in include_fields:
        session_args[field] = fields_sum[f"{field}__sum"]
    return model.objects.update_or_create(session=month, year=year, unit=UnitType.TOTAL, defaults=session_args)


def quarter_calc(model, month, year, unit):
    return session_wise_calc(model, month, year, unit, 3)


def half_calc(model, month, year, unit):
    return session_wise_calc(model, month, year, unit, 6)


def chain_reaction(model, month, year, unit):
    quarter_calc(model, month, year, unit)
    half_calc(model, month, year, unit)

    # monthly calculations
    calc_monthly_total(model, month, year)
    quarter_calc(model, month, year, 2)
    half_calc(model, month, year, 2)
