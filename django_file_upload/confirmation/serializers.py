from rest_framework import serializers

from django_file_upload.confirmation.models import BuyerWise


class BuyerWiseSerializer(serializers.ModelSerializer):

    session = serializers.CharField(source='get_session_display')

    class Meta:
        model = BuyerWise
        exclude = []
