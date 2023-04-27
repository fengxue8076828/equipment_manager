from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Module(models.Model):
    name=models.CharField(max_length=50)
    parent_module=models.ForeignKey("self",blank=True,null=True,on_delete=models.SET_NULL)
    icon=models.CharField(max_length=100,null=True,blank=True)
    link=models.CharField(max_length=50,null=True,blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Role(models.Model):
    name=models.CharField(max_length=20)
    modules=models.ManyToManyField(Module)

    def __str__(self):
        return self.name

class User(AbstractUser):
    role=models.ForeignKey(Role,blank=True,null=True,on_delete=models.SET_NULL)
    real_name=models.CharField(max_length=10)
    fix_phone_number=models.CharField(max_length=20)
    cellphone_number=models.CharField(max_length=20)
    photo=models.ImageField(upload_to="user-images/")

    def __str__(self):
        return self.username
    
class EquipCategory(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Warehouse(models.Model):
    number = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    



