from rest_framework.generics import ListAPIView

from django_file_upload.confirmation.models import BuyerWiseCon
from django_file_upload.confirmation.serializers import BuyerWiseSerializer


class BuyerWiseView(ListAPIView):
    serializer_class = BuyerWiseSerializer
    queryset = BuyerWiseCon.objects.all()
