from django import forms
from .models import DeviceMalfuntionRecord, MaintainanceRecord


class DeviceMalfunctionRecordForm(forms.ModelForm):
    class Meta:
        model = DeviceMalfuntionRecord
        fields = [
            "title",
            "description",
        ]


class MaintainanceRecordForm(forms.ModelForm):
    is_finished = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    class Meta:
        model = MaintainanceRecord
        fields = [
            "title",
            "description",
            "is_finished",
        ]
