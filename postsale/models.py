from django.db import models
from presale.models import Device
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
User = get_user_model()

class Client(models.Model):

    name = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    email = models.CharField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=300)
    memo = models.CharField(max_length=1000)

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
         ("good","正常")
    ]

    device = models.OneToOneField(Device,on_delete=models.CASCADE,related_name="device_sold")
    outbound = models.ForeignKey(OutBound,null=True,on_delete=models.CASCADE)
    fix_address = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=30,null=True,choices=state_choices)

    def __str__(self):
        return self.device.equipment.name
    

