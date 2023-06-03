from django.db import models
from authentication.models import User
# Create your models here.



class RiderManager(models.Manager):
    def get_queryset(self,*args,**kawargs):
        return super().get_queryset(*args,**kawargs).filter(type=User.Types.RIDER)
    def create_user(self,username,email,password=None):
        # return User.objects.create_user(username,email,password)
        rider=self.model(username=username,email=email)
        rider.set_password(password)
        rider.save()
        return rider


class Rider(User):
    objects=RiderManager()
    class Meta:#proxy models they don't create new tables same table of the User table
        proxy=True

    def save(self,*args,**kwargs):
        if not self.pk:#if record doesn't exist
            self.type=User.Types.RIDER
        
        return super().save(*args,**kwargs)
    
    def serialize(self):
        return {
            'username':self.username,
            'email':self.email,
        }


