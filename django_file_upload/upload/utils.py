from math import isnan

from django_file_upload.confirmation.models import Buyer, BuyerWiseCon


def clean_dict(value):
    cleaned_dict = {k: value[k] for k in value if (isinstance(value[k], float) or
                                                   isinstance(value[k], int)) and not isnan(value[k])}
    return cleaned_dict


def insert_data(model, payload):

    for value in payload:
        cleaned_dict = clean_dict(value=value)
        print("Cleaned dict: ", cleaned_dict)
        model.objects.create(**cleaned_dict)


def insert_buyer_wise_data(payload):

    for value in payload:
        buyer_name = value.pop("buyer")
        obj, created = Buyer.objects.get_or_create(name=buyer_name)
        BuyerWiseCon.objects.create(buyer=obj, **value)
