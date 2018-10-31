from rest_framework import serializers

from django_file_upload.confirmation.models import BuyerWise


class BuyerWiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuyerWise
        exclude = []


