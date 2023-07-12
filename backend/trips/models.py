from django.contrib.gis.db import models
from rider.models import Rider
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Trips(models.Model):
    class Trip_Status(models.TextChoices):
        BOOKED='BOOKED'
        CANCELLED='CANCELLED'
        COMPLETED='COMPLETED'
        ONGOING='ONGOING'
        NA='NA'
    rider=models.ForeignKey(Rider,on_delete=models.CASCADE,related_name="rider_trips")
    driver=models.ForeignKey('driver.Driver',on_delete=models.CASCADE,related_name="trips")
    time_start=models.DateField(auto_created=True,auto_now_add=True)
    time_completed=models.DateField(default=None,null=True,blank=True)
    duration=models.TimeField(default=None,null=True,blank=True)
    status=models.CharField(_('Status'),max_length=20,choices=Trip_Status.choices,default=Trip_Status.NA)
    origin=models.PointField()
    destination=models.PointField()


    def serialize(self):
        return {
    "tripId":self.id,
    "rider":self.rider.username,
    "driver name":self.driver.username,
    "carId":self.driver.id,
    "car Type":self.driver.carType,
    "car Number":self.driver.carNumber,
    "car Model":self.driver.carModel,
    "time start":str(self.time_start),
    "origin":{"longitude":self.origin[0],"latitude":self.origin[1]},
    "destination":{"longitude":self.destination[0],"latitude":self.destination[1]},
    "status":self.status
        }

    def __str__(self):
        return f"Trip Id:{self.id}" #will change to uuid