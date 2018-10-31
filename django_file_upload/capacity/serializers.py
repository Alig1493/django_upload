from rest_framework import serializers

from django_file_upload.capacity.models import MachineDay, SAH, Pcs, GGPcs


class MachineDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = MachineDay
        exclude = []


class SAHSerializer(serializers.ModelSerializer):

    class Meta:
        model = SAH
        exclude = []


class PcsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pcs
        exclude = []


class GGPcsSerializers(serializers.ModelSerializer):

    class Meta:
        model = GGPcs
        exclude = []
