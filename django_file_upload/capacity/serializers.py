from rest_framework import serializers

from django_file_upload.capacity.models import MachineDay, SAH, Pcs, GGPcs


class MachineDaySerializer(serializers.ModelSerializer):

    session = serializers.CharField(source='get_session_display')

    class Meta:
        model = MachineDay
        exclude = []


class SAHSerializer(serializers.ModelSerializer):

    session = serializers.CharField(source='get_session_display')

    class Meta:
        model = SAH
        exclude = []


class PcsSerializer(serializers.ModelSerializer):

    session = serializers.CharField(source='get_session_display')

    class Meta:
        model = Pcs
        exclude = []


class GGPcsSerializers(serializers.ModelSerializer):

    session = serializers.CharField(source='get_session_display')

    class Meta:
        model = GGPcs
        exclude = []
