from django.db import models
from rider.models import Rider
from driver.models import Driver

# Create your models here.
class RiderClientChannel(models.Model):
    channel_name=models.CharField(max_length=128,blank=False,null=False)
    rider=models.OneToOneField(Rider,on_delete=models.CASCADE,related_name='channel',blank=False,null=False,unique=True)

class DriverClientChannel(models.Model):
    channel_name=models.CharField(max_length=128,blank=False,null=False)
    driver=models.OneToOneField(Driver,on_delete=models.CASCADE,related_name='channel',blank=False,null=False,unique=True)


#Sharding of the db based on the location 
#Efficiency of the data fetching improved by grids maps mapped with  sharded db
#Every grid contains a grid id and based on strategy is mapped to a sharded db
