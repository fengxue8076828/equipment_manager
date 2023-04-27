from django import forms
from .models import DeviceSold,OutBound
from django.contrib.auth import get_user_model

User = get_user_model()

class DeviceSoldForm(forms.ModelForm):
    class Meta:
        model = OutBound
        fields = [
            'outbound_image',
            'buyer',
            'pay_state',
            'pay_date'
        ]

class DeviceSoldUpdateForm(forms.ModelForm):
    maintainer = forms.ModelChoiceField(User.objects.filter(role__id=4))
    class Meta:
        model = DeviceSold
        fields =[
            'fix_address',
            'state'
        ]