from rest_framework import serializers
from presale.models import Device, Equipment
from maintainance.models import DeviceMalfuntionRecord, MaintainanceRecord
from info_manager.models import Warehouse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "real_name",
        ]


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            "name",
            "model",
        ]


class DeviceSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = Device
        fields = [
            "id",
            "equipment",
            "hardware_serial",
            "software_serial",
            "warehouse",
            "maintainer",
            "state",
        ]


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            "id",
            "number",
            "name",
        ]


class DeviceMalfunctionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceMalfuntionRecord
        fields = [
            "id",
            "title",
            "description",
            "device",
        ]
        read_only_fields = (
            "device",
            "operator",
            "maintainer",
            "dispatch_date",
        )


class MaintainanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintainanceRecord
        fields = [
            "title",
            "description",
            "malfunction_record",
            "date",
        ]
        read_only_fields = ["malfunction_record", "date"]
