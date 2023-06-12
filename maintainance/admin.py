from django.contrib import admin
from .models import MaintainanceRecord,DeviceMalfuntionRecord

# Register your models here.
admin.site.register(DeviceMalfuntionRecord)
admin.site.register(MaintainanceRecord)