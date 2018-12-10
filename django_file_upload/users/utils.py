from django.db.models import Case, When, Sum

from django_file_upload.capacity.models import MachineDay, SAH, Pcs, GGPcs
from django_file_upload.confirmation.models import BuyerWiseCon
from django_file_upload.core.config import UnitType
from django_file_upload.core.utils import get_include_fields


def get_models():
    return [MachineDay, SAH, Pcs, GGPcs, BuyerWiseCon]


def get_model_fields(unit, **kwargs):
    data = {}
    data_total = {}
    for model in get_models():

        queryset = model.objects.none()

        for index in range(2):

            year = kwargs.get("year")
            session_list = kwargs['session__in'][:9]

            if index > 0:
                year = year + 1
                session_list = kwargs['session__in'][9:]

            # print("Index: ", index)
            # print("QUerying for year: ", year)

            # preserved = Case(*[When(session=session, then=pos) for pos, session in enumerate(session_list)])

            queryset |= (model.objects.filter(unit=unit, year=year, session__in=session_list)
                                      .order_by("-created_at")
                                      .order_by("session")
                                      .distinct("session"))

            # if model._meta.model_name == MachineDay._meta.model_name:
            #
            #     if year == 2019:
            #         print(model.objects.filter(unit=unit, year=year, session__in=session_list)
            #                               .order_by("-created_at")
            #                               .order_by("session")
            #                               .distinct("session").values("budget", "session"))
            #     print(session_list)
            #     print("Total queryset:", queryset.values("budget", "session"))

        include_fields = get_include_fields(model=model)
        aggregate_args = [Sum(x) for x in include_fields]
        print("Aggregate args:", aggregate_args)

        fields_sum = (model.objects.filter(id__in=queryset.values_list("id", flat=True))
                                   .exclude(session__gt=12).aggregate(*aggregate_args))
        print("Fields sum:", fields_sum)

        data[model] = queryset
        data_total[model] = fields_sum

        # if model._meta.model_name == MachineDay._meta.model_name:
        #     print("Inside data generation")
        #     print(data)
        #     for k, v in data.items():
        #         print("Keys:\n", k)
        #         print("Values:\n", v.values())

    return data, data_total


def get_unit_models(**kwargs):
    data = {
        UnitType.AUTO: get_model_fields(UnitType.AUTO, **kwargs),
        UnitType.SEMI: get_model_fields(UnitType.SEMI, **kwargs),
        UnitType.TOTAL: get_model_fields(UnitType.TOTAL, **kwargs),
    }

    # print("======================================")
    # print("======================================")
    # print("======================================")
    # print("======================================")
    # print("Inside utils unit models")
    # print(data)
    # print("======================================")
    # print("======================================")
    # print("======================================")
    # print("======================================")

    return data
