from django_jinja import library

from django_file_upload.confirmation.models import BuyerWiseCon
from django_file_upload.core.config import EXCLUDE_FIELDS, Session


@library.global_function
def get_model_name(value):
    return value._meta.vebose_name


@library.global_function
def get_field_value(data, field):

    value = getattr(data, field)
    # if type(data) == SAH and field == "budget" and data.unit == UnitType.AUTO:
        # print("Data: ", data)
        # print("Field: ", field)
        # print("Value: ", value)
    return round(value, 2) if value is not None else ''


@library.global_function
def allowed_field(value):
    return value not in EXCLUDE_FIELDS


@library.global_function
def get_session_name(number):
    return Session.CHOICES[number-1][1]


@library.global_function
def get_session_class(number):

    # print("================================================")
    # print("Session name:", Session.CHOICES[number - 1][1])
    # print("================================================")

    return "m" if number <= 12 else "o"


@library.global_function
def is_buyerwise(data):
    if isinstance(data, str):
        return data == BuyerWiseCon._meta.model_name
    return isinstance(data, BuyerWiseCon)


@library.global_function
def debugger(data):
    print("Inside template debugger")
    print(data)


@library.global_function
def get_field_total(field_name, total_dict):
    # print("Inside getting field total")
    # print(total_dict)
    # # print(getattr(total_dict, f"{field_name}__sum"))
    # print(total_dict.get(f"{field_name}__sum"))
    return total_dict.get(f"{field_name}__sum")


@library.global_function
def get_buyer_total(queryset):

    field = "total"
    if queryset.model == BuyerWiseCon:
        field = "confirmed"

    overall_sum = 0
    overall_values = queryset.filter(session__lt=13).values_list(field, flat=True)

    # if field == "total":
    #     print("Queryset values:", queryset.values())
    #     print("overall values:", overall_values)

    if overall_values:
        for value in overall_values:
            overall_sum += value

    return overall_sum


@library.filter
def format_value(value):
    if not value or value == "":
        return ""
    return round(value) if isinstance(value, float) else value
