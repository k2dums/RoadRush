from django.db import models
from driver.models import Driver
from rider.models import Rider

# Create your models here.

class Trips(models.Model):
    class Trip_Status:
        CANCELLED='cancelled'
        COMPLETED='completed'
        ONGOING='ongoing'
    rider=models.ForeignKey(Rider,on_delete=models.CASCADE,related_name="rider_trips")
    driver=models.ForeignKey(Driver,on_delete=models.CASCADE,related_name="driver_trips")
    time_start=models.DateField(auto_created=True)
    time_completed=models.DateField(default=None)
    duration=models.TimeField(default=None)
    status=Trip_Status.ONGOING

