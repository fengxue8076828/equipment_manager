from django.db import models
from presale.models import Device
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
User = get_user_model()

class Client(models.Model):
    
    pay_method_choices = [
        ('instant_pay','立即结算'),
        ('month_pay','按月结算'),
        ('season_pay','按季度结算'),
        ('year_pay','按年结算'),
    ]

    name = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    email = models.CharField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=300)
    memo = models.CharField(max_length=1000)
    pay_method = models.CharField(max_length=30,choices=pay_method_choices)

    def __str__(self):
        return self.name
    
class OutBound(models.Model):
    pay_state_choices = [
        ('paid','已结算'),
        ('unpaid','未结算'),
    ]
    outbound_number = models.CharField(max_length=100,null=True)
    outbound_operator = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="devices_sold")
    outbound_date = models.DateField(null=True)
    outbound_image = models.ImageField(upload_to="outbound-images/")
    buyer =  models.ForeignKey(Client,null=True,blank=True,on_delete=models.SET_NULL,related_name="devices_bought")
    pay_state = models.CharField(max_length=30,choices=pay_state_choices)
    pay_date = models.DateField(default=timezone.now().date())

    def __str__(self):
            return self.outbound_number
    

class DeviceSold(models.Model):

    state_choices = [
        ("good","正常"),
        ("bad","故障"),
        ("maintaining","检修中")
    ]

    device = models.OneToOneField(Device,on_delete=models.CASCADE)
    outbound = models.ForeignKey(OutBound,null=True,on_delete=models.CASCADE)
    fix_address = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=30,choices=state_choices,null=True)

    def __str__(self):
        return self.device.equipment.name
    

