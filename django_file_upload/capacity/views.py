from rest_framework.generics import ListAPIView

from django_file_upload.capacity.models import MachineDay, SAH, Pcs, GGPcs
from django_file_upload.capacity.serializers import MachineDaySerializer, SAHSerializer, PcsSerializer, GGPcsSerializers


class MachineDayView(ListAPIView):
    serializer_class = MachineDaySerializer
    queryset = MachineDay.objects.all()


class SAHView(ListAPIView):
    serializer_class = SAHSerializer
    queryset = SAH.objects.all()


class PcsView(ListAPIView):
    serializer_class = PcsSerializer
    queryset = Pcs.objects.all()


class GGPcsView(ListAPIView):
    serializer_class = GGPcsSerializers
    queryset = GGPcs.objects.all()
