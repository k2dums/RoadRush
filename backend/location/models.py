from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from driver.models import Driver
# Create your models here.

#This table is for the driver location
class Location(models.Model):
    location=models.PointField()
    driver=models.OneToOneField(Driver,on_delete=models.CASCADE,related_name='driver_location')
    