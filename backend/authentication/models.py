from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
#WE NEED TO TELL DJANGO TO USE THE MODEL, go to setting > AUTH_USER_MODEl='authentication.User' ie app.Model


#Creating custom user
#Allows us to run queries
class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if username is None:
            raise TypeError('User should have username')
        if email is None:
            raise TypeError('User should have email')   
        if password is None:
            raise TypeError('Password should not be None')
        #Need to define how a user should be created
        user=self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        #because while creating in serializer it needs to return
        return user

    def create_superuser(self,username,email,password=None):
        if  password is None:
            raise TypeError('Password should not be none') 
        
        #Need to define how a supseruser should be created
        user=self.create_user(username,email,password)
        user.is_superuser=True
        user.is_staff=True
        user.type=User.Types.NONE
        user.save()
       
        return user #Why are we returing the user here in create_superuser()?

#inherit AbstractBaseUser giving acess to regular user fields. PermissionMixin 
class User(AbstractBaseUser,PermissionsMixin):
    class UserTypes(models.TextChoices):
        RIDER='RIDER','Rider'
        DRIVER='DRIVER','Driver'
        NONE='NONE','None'

    type=models.CharField(_('UserType'),max_length=50,choices=UserTypes.choices,default=UserTypes.RIDER)
    username=models.CharField(max_length=255,unique=True,db_index=True) #db_index True ,making indexable makes searching on username fast
    email=models.EmailField(max_length=255,unique=True,db_index=True)
    is_verified=models.BooleanField(default=False)#to know if the user is verified or not
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    # defining what attributes the user will use to log in
    USERNAME_FIELD='email' #by default django will expect to send username
    #next we are defining the required fields
    REQUIRED_FIELDS=['username','password']

    #telling django how to manage the object
    objects=UserManager()

    def __str__(self):
        return self.email
    

    #token helps to do something with user and user
    def tokens(self):
        # will return user token
        tokens=RefreshToken.for_user(self)
        return{
            'refresh':str(tokens),#will be an instance of access token that is why we str convert
            'access':str(tokens.access_token)
        }
    


