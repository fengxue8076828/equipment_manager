from django import forms
from .models import DeviceSold, OutBound, Client
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = "date"


class DeviceSoldForm(forms.ModelForm):
    pay_date = forms.DateField(widget=DateInput())

    class Meta:
        model = OutBound
        fields = ["outbound_image", "buyer", "pay_state", "pay_date"]


class DeviceSoldUpdateForm(forms.ModelForm):
    maintainer = forms.ModelChoiceField(User.objects.filter(role__id=4))

    class Meta:
        model = DeviceSold
        fields = [
            "fix_address",
            "state",
        ]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "name",
            "telephone",
            "email",
            "address",
            "memo",
        ]
