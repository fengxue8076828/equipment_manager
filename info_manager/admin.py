from django.contrib import admin
from .models import User,Role,Module,EquipCategory,Warehouse

# Register your models here.

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Module)
admin.site.register(EquipCategory)
admin.site.register(Warehouse)