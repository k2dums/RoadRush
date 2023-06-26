from django.contrib.gis.db import models
from driver.models import Driver
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
    driver=models.ForeignKey(Driver,on_delete=models.CASCADE,related_name="driver_trips")
    time_start=models.DateField(auto_created=True)
    time_completed=models.DateField(default=None)
    duration=models.TimeField(default=None)
    status=models.CharField(_('Status'),max_length=20,choices=Trip_Status.choices,default=Trip_Status.NA)
    origin=models.PointField()
    destination=models.PointField()

