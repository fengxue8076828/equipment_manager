from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, Module, EquipCategory, Warehouse
from .forms import UserChangeAdminForm

# Register your models here.


class CustomedUserAdmin(UserAdmin):
    form = UserChangeAdminForm
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {"fields": ("real_name", "fix_phone_number", "cellphone_number", "role")},
        ),
    )


admin.site.register(User, CustomedUserAdmin)
admin.site.register(Role)
admin.site.register(Module)
admin.site.register(EquipCategory)
admin.site.register(Warehouse)
