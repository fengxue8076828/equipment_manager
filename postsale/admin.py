from django.contrib import admin
from .models import DeviceSold,Client,OutBound

# Register your models here.

admin.site.register(DeviceSold)
admin.site.register(Client)
admin.site.register(OutBound)