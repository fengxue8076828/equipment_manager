from django.db import models
from info_manager.models import EquipCategory
from info_manager.models import Warehouse
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.

User = get_user_model()

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    email = models.CharField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=300)
    memo = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    category=models.ForeignKey(EquipCategory,null=True,blank=True,on_delete=models.SET_NULL)
    supplier = models.ForeignKey(Supplier,null=True,blank=True,on_delete=models.SET_NULL)
    model = models.CharField(max_length=100)
    hardware_serial = models.CharField(max_length=200)
    software_serial = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    sale_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return self.name
    
class Inbound(models.Model):
    equipment = models.ForeignKey(Equipment,null=True,on_delete=models.SET_NULL)
    supplier = models.ForeignKey(Supplier,null=True,on_delete=models.SET_NULL)
    warehouse = models.ForeignKey(Warehouse,null=True,on_delete=models.SET_NULL)
    amount = models.IntegerField(default=1)
    inbound_number = models.CharField(max_length=100)
    inbound_operator = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="devices_inbound")
    inbound_date = models.DateField()
    inbound_image = models.ImageField(upload_to="inbound-images/")

    def __str__(self):
        return self.inbound_number
    
class Device(models.Model):
    
    state_choices = [
        ("ready_excellent","可发货(好)"),
        ("ready_good","可发货(中)"), 
        ("ready","可发货"),
        ("ready_confirm","可发货，需确认"),
        ("under_maintain","检修中"),
        ("ordered","已订货"),
        ("sold","已售出"),    
    ]
    supplier = models.ForeignKey(Supplier,null=True,on_delete=models.SET_NULL)
    maintainer = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="maintain_devices")
    equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE,related_name="devices")
    warehouse=models.ForeignKey(Warehouse,null=True,blank=True,on_delete=models.SET_NULL,related_name="devices")
    state = models.CharField(max_length=100,choices=state_choices)
    inbound=models.ForeignKey(Inbound,null=True,on_delete=models.SET_NULL)


    class Meta:
        verbose_name_plural = "Devices"

    def __str__(self):
        return self.equipment.name


