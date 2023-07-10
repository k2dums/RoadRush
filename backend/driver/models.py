# from django.db import models
from django.contrib.gis.db import models
from authentication.models import User
from trips.models import Trips
from django.contrib.gis.geos import Point
from django.utils.translation import gettext_lazy as _
# Create your models here.


class DriverManager(models.Manager):
    def get_queryset(self,*args,**kawargs):
        return super().get_queryset(*args,**kawargs).filter(type=User.UserTypes.DRIVER)
    def create_user(self,username,email,password,carId,carModel,carNumber):
        driver=self.model(username=username,email=email,carId=carId,carModel=carModel,carNumber=carNumber,location=Point(12,12,srid=4236))
        driver.set_password(password)
        driver.save()
        return driver

class Driver(User):

    class CarTypes(models.TextChoices):
        NORMAL='NORMAL','Normal'
        LUXURY='LUXURY','Luxury'
    objects=DriverManager()
    carId=models.CharField(max_length=256,default='NA',unique=True,)
    carModel=models.CharField(max_length=256,default='NA')
    carNumber=models.CharField(max_length=256,default='Na')
    location=models.PointField()
    occupiedStatus=models.BooleanField(default=False)
    carType=models.CharField(_('CarType'),max_length=20,choices=CarTypes.choices,default=CarTypes.NORMAL)
    currentTrip=models.ForeignKey(Trips,null=True,on_delete=models.SET_NULL,blank=True,related_name='driverofTrip',)
    def save(self,*args,**kwargs):
        self.type=User.UserTypes.DRIVER
        return super().save(*args,**kwargs)
    
    def serialize(self):
        return {
            'username':self.username,
            'email':self.email,
            'carId':self.carId,
            'carNumber':self.carNumber,
            'carModel':self.carModel,
        }

