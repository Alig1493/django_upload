from django.db.models import Case, When

from django_file_upload.capacity.models import MachineDay, SAH, Pcs, GGPcs
from django_file_upload.confirmation.models import BuyerWiseCon
from django_file_upload.core.config import UnitType


def get_models():
    return [MachineDay, SAH, Pcs, GGPcs, BuyerWiseCon]


def get_model_fields(unit, **kwargs):
    data = {}
    for model in get_models():
        preserved = Case(*[When(session=session, then=pos) for pos, session in enumerate(kwargs['session__in'])])
        data[model] = (model.objects.filter(unit=unit, **kwargs)
                       .order_by(preserved)
                       .order_by("-created_at")
                       .order_by("session")
                       .distinct("session")
                       # .order_by('session', '-created_at')
                       # .distinct('session')
                       )
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
