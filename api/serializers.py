from rest_framework import serializers
from presale.models import Device
from maintainance.models import DeviceMalfuntionRecord, MaintainanceRecord


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "id",
            "equipment",
            "warehouse",
            "state",
        ]


class DeviceMaintainanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceMalfuntionRecord
        fields = [
            "device",
            "title",
            "description",
            "state",
        ]


class MaintainanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintainanceRecord
        fields = [
            "title",
            "description",
            "date",
        ]
