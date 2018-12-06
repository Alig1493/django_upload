from math import isnan

from django_file_upload.confirmation.models import Buyer, BuyerWiseCon, BuyerWiseTotal
from django_file_upload.core.config import Session, UnitType


def get_adjusted_session(session):

    max_month = 12
    session += 6

    if session > max_month:
        session -= 12

    return session


def clean_dict(value):
    cleaned_dict = {k: value[k] for k in value if (isinstance(value[k], float) or
                                                   isinstance(value[k], int)) and not isnan(value[k])}
    print("Previous session: ", cleaned_dict["session"])
    cleaned_dict["session"] = get_adjusted_session(session=cleaned_dict["session"])
    print("New session: ", cleaned_dict["session"])
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

    years = BuyerWiseCon.objects.distinct("year").values_list("year", flat=True)
    print("Calculating for years: ", years)

    for year in years:
        print("Going for year", year)
        for unit in UnitType.CHOICES:
            print("Going for unit", unit)
            for session in Session.get_session_list():
                print("Going for Session", session)
                # calculate total of the month for all the buyers
                total_value = BuyerWiseCon.month_total(unit=unit[0], session=session[0], year=year)

                defaults = {
                    "unit": unit[0],
                    "session": session[0],
                    "year": year
                }

                # create total for each month of the individual buyer
                buyerwise_total = BuyerWiseTotal.objects.filter(**defaults)

                if buyerwise_total.exists():
                    print("Buyerwise total exist so updating")
                    buyerwise_total.update(total=total_value)
                else:
                    print("Buyerwise total doesn't exist so Creating")
                    BuyerWiseTotal.objects.create(total=total_value, **defaults)

                if defaults["year"] == 2018:
                    print(BuyerWiseTotal.objects.filter(**defaults).values_list("total", "session", "unit", "year"))
                    print(session)
                    print(unit)
                    print(buyerwise_total)
                    print(total_value)
            print(BuyerWiseTotal.objects.filter(year=year, unit=unit[0])
                  .values_list("total", "session", "unit", "year").count())
