from django import forms
from .models import Equipment, Device, Inbound, Supplier
from django.contrib.auth import get_user_model
from info_manager.models import EquipCategory

User = get_user_model()


class EquipmentForm(forms.ModelForm):
    category = forms.ModelChoiceField(EquipCategory.objects.exclude(parent=None))

    class Meta:
        model = Equipment
        fields = [
            "name",
            "category",
            "model",
            "price",
            "sale_price",
        ]


class DeviceForm(forms.ModelForm):
    maintainer = forms.ModelChoiceField(User.objects.filter(role__id=4))

    class Meta:
        model = Device
        fields = [
            "equipment",
            "warehouse",
            "maintainer",
            "hardware_serial",
            "software_serial",
        ]


class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = [
            "equipment",
            "supplier",
            "warehouse",
            "amount",
            "inbound_image",
        ]


class DeviceUpdateForm(forms.ModelForm):
    maintainer = forms.ModelChoiceField(User.objects.filter(role__id=4))

    class Meta:
        model = Device
        fields = [
            "state",
            "maintainer",
            "warehouse",
            "hardware_serial",
            "software_serial",
        ]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "name",
            "telephone",
            "email",
            "address",
            "memo",
        ]
