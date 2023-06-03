# from django.db import models
from django.contrib.gis.db import models
from authentication.models import User
from django.contrib.gis.geos import Point
# Create your models here.


class DriverManager(models.Manager):
    def get_queryset(self,*args,**kawargs):
        return super().get_queryset(*args,**kawargs).filter(type=User.Types.DRIVER)
    def create_user(self,username,email,password,carId,carModel,carNumber):
        driver=self.model(username=username,email=email,carId=carId,carModel=carModel,carNumber=carNumber,location=Point(12,12,srid=4236))
        driver.set_password(password)
        driver.save()
        return driver

class Driver(User):
    objects=DriverManager()
    carId=models.CharField(max_length=256,default='NA',unique=True,)
    carModel=models.CharField(max_length=256,default='NA')
    carNumber=models.CharField(max_length=256,default='Na')
    location=models.PointField()
    occupiedStatus=models.BooleanField(default=False)
    

    def save(self,*args,**kwargs):
        print("pk",self.pk)
        self.type=User.Types.DRIVER
        return super().save(*args,**kwargs)
    
    def serialize(self):
        return {
            'username':self.username,
            'email':self.email,
            'carId':self.carId,
            'carNumber':self.carNumber,
            'carModel':self.carModel,
        }

