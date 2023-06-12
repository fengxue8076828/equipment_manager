from django.db import models
from presale.models import Device
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class DeviceMalfuntionRecord(models.Model):
    state_choices = [
        ("assigned", "已分配"),
        ("started", "已开始检修"),
        ("finished", "已完成"),
    ]
    device = models.ForeignKey(Device, null=True, on_delete=models.SET_NULL)
    operator = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="operator"
    )
    maintainer = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="maintainer"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    dispatch_date = models.DateField(null=True)
    state = models.CharField(max_length=50, default="assigned", choices=state_choices)

    def __str__(self):
        return self.title


class MaintainanceRecord(models.Model):
    malfunction_record = models.ForeignKey(
        DeviceMalfuntionRecord,
        null=True,
        on_delete=models.SET_NULL,
        related_name="maintainance_records",
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    date = models.DateField(null=True)

    def __str__(self):
        return self.title
