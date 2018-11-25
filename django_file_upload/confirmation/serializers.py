from rest_framework import serializers

from django_file_upload.confirmation.models import BuyerWiseCon


class BuyerWiseSerializer(serializers.ModelSerializer):

    session = serializers.CharField(source='get_session_display')

    class Meta:
        model = BuyerWiseCon
        exclude = []
