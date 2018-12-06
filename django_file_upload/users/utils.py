from django.db.models import Case, When

from django_file_upload.capacity.models import MachineDay, SAH, Pcs, GGPcs
from django_file_upload.confirmation.models import BuyerWiseCon
from django_file_upload.core.config import UnitType


def get_models():
    return [MachineDay, SAH, Pcs, GGPcs, BuyerWiseCon]


def get_model_fields(unit, **kwargs):
    data = {}
    for model in get_models():

        queryset = model.objects.none()

        for index in range(2):

            year = kwargs.get("year")
            session_list = kwargs['session__in'][:9]

            if index > 0:
                year = year + 1
                session_list = kwargs['session__in'][9:]

            print("Index: ", index)
            print("QUerying for year: ", year)

            preserved = Case(*[When(session=session, then=pos) for pos, session in enumerate(session_list)])

            queryset |= (model.objects.filter(unit=unit, year=year)
                                      .order_by(preserved)
                                      .order_by("-created_at")
                                      .order_by("session")
                                      .distinct("session"))

        data[model] = queryset

        if isinstance(model, BuyerWiseCon):
            print("Inside data generation")
            print(data)
    return data


def get_unit_models(**kwargs):
    data = {
        UnitType.AUTO: get_model_fields(UnitType.AUTO, **kwargs),
        UnitType.SEMI: get_model_fields(UnitType.SEMI, **kwargs),
        UnitType.TOTAL: get_model_fields(UnitType.TOTAL, **kwargs),
    }
    return data
