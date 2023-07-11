from django.db import models
from authentication.models import User
# from trips.models import Trips
# Create your models here.



class RiderManager(models.Manager):
    def get_queryset(self,*args,**kawargs):
        return super().get_queryset(*args,**kawargs).filter(type=User.UserTypes.RIDER)
    def create_user(self,username,email,password=None):
        # return User.objects.create_user(username,email,password)
        rider=self.model(username=username,email=email)
        rider.set_password(password)
        rider.save()
        return rider


class Rider(User):
    objects=RiderManager()
    # class Meta:#proxy models they don't create new tables same table of the User table
    #     proxy=True

    onTrip=models.BooleanField(default=False)
    currentTrip=models.ForeignKey('trips.Trips',null=True,blank=True,on_delete=models.SET_NULL,related_name='riderofTrip')
    def save(self,*args,**kwargs):
        self.type=User.UserTypes.RIDER
        return super().save(*args,**kwargs)
    
    def serialize(self):
        return {
            'username':self.username,
            'email':self.email,
            'onTrip':self.onTrip,
            'currentTrip':str(self.currentTrip)
        }
    
    def __str__(self):
        return f"{self.username}"


