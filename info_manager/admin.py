from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, Module, EquipCategory, Warehouse
from .forms import UserCreateForm

# Register your models here.


class CustomedUserAdmin(UserAdmin):
    list_display = [
        "username",
        "real_name",
    ]


admin.site.register(User, CustomedUserAdmin)
admin.site.register(Role)
admin.site.register(Module)
admin.site.register(EquipCategory)
admin.site.register(Warehouse)
