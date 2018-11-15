from django_jinja import library

from django_file_upload.capacity.models import SAH
from django_file_upload.core.config import EXCLUDE_FIELDS, Session


@library.global_function
def get_model_name(value):
    return value._meta.vebose_name


@library.global_function
def get_field_value(data, field):

    value = getattr(data, field)
    if type(data) == SAH and field == "budget":
        print("Data: ", data)
        print("Field: ", field)
        print("Value: ", value)
    return round(value, 2) if value is not None else ''


@library.global_function
def allowed_field(value):
    return value not in EXCLUDE_FIELDS


@library.global_function
def get_session_name(number):
    return Session.CHOICES[number-1][1]


@library.global_function
def get_session_class(number):
    return "m" if number <= 12 else "o"
