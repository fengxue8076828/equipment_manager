from django.contrib import admin
from .models import Equipment,Device,Supplier,Inbound
# Register your models here.

admin.site.register(Equipment)
admin.site.register(Device)
admin.site.register(Supplier)
admin.site.register(Inbound)