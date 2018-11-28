from math import isnan

from django_file_upload.confirmation.models import Buyer, BuyerWiseCon, BuyerWiseTotal
from django_file_upload.confirmation.utils import buyer_chain_reaction
from django_file_upload.core.config import Session, UnitType


def clean_dict(value):
    cleaned_dict = {k: value[k] for k in value if (isinstance(value[k], float) or
                                                   isinstance(value[k], int)) and not isnan(value[k])}
    return cleaned_dict


def insert_data(model, payload):

    for value in payload:
        cleaned_dict = clean_dict(value=value)
        # print("Cleaned dict: ", cleaned_dict)
        model.objects.create(**cleaned_dict)


def insert_buyer_wise_data(payload):

    for value in payload:
        buyer_name = value.pop("buyer")
        buyer, created = Buyer.objects.get_or_create(name=buyer_name)
        # print("Buyer name: ", buyer)
        # print("Buyer created: ", created)
        BuyerWiseCon.objects.create(buyer=buyer, **value)
        # buyer_chain_reaction(model=BuyerWiseCon,
        #                      month=buyer_wise_con.session,
        #                      year=buyer_wise_con.year,
        #                      unit=buyer_wise_con.unit,
        #                      buyer=buyer)


def calculate_monthly_totals():

    for year in BuyerWiseCon.objects.distinct("year").values_list("year", flat=True):
        for unit in UnitType.CHOICES:
            for session in Session.get_session_list():
                # calculate total of the month for all the buyers
                total_value = BuyerWiseCon.month_total(unit=unit[0], session=session[0], year=year)

                defaults = {
                    "unit": unit[0],
                    "session": session[0],
                    "year": year
                }

                # create total for each month of the individual buyer
                buyerwise_total, created = BuyerWiseTotal.objects.update_or_create(total=total_value, defaults=defaults)

                if defaults["unit"] == 0 and defaults["session"] == 2 and defaults["year"] == 2018:
                    print("Showing details for buyer total for february 2018 semi auto")
                    print(buyerwise_total)
                    print(created)
