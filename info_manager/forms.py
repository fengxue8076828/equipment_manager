from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import EquipCategory,Warehouse

User=get_user_model()

class CustomedAuthenticationForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'username',
            'real_name',
            'fix_phone_number',
            'cellphone_number',
            'email',
            'photo'
        ]
    
class UserCreateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'username',
            'real_name',
            'fix_phone_number',
            'cellphone_number',
            'email',
            'role'
        ]

class EquipCategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=EquipCategory.objects.filter(parent=None),
        empty_label="请选择一个一级分类(不选创建一级分类)",
        required=False
    )
    class Meta:
        model=EquipCategory

        fields=[
            'parent',
            'name',
            'description'
        ]

class WarehouseForm(forms.ModelForm):
    class Meta:
        model=Warehouse
        fields = [
            "number",
            "name",
            "description",
            "location",
        ]

