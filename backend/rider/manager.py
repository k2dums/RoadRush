from rider.models import Rider
from authentication.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class RiderManager:
    @classmethod
    def getRider(cls,username):
        """Returns the rider objects"""
        riderObj=Rider.objects.get(username=username)
        assert isinstance(riderObj,Rider)
        return riderObj
    @classmethod
    def riderDetails(cls,username):
        """Returns the Rider details such as username and if ratings"""
        user=Rider.objects.get(username=username)
        return {
            'username':user.username,
            'email':user.email,
        }
        
    @classmethod
    def registerRider(cls,username,email,password):
        if Rider.objects.filter(username=username).exists():
            return {'error':'username already taken'}
        if Rider.objects.filter(email=email).exists():
            return {'error':'email already taken'}
        if not(email):
            return {'error':'email is empty'}
        if not(username):
            return {'error':'username is empty'}
        if not(password):
            return {'error':'password is empty'}
        if len(password)<6:
            return {'error':'password length less than 6'}
        try:
            validate_email(email)
        except ValidationError:
            return {'error':'email not valid'}
        try:
            rider=Rider.objects.create_user(username=username,email=email,password=password)
            return rider
        except Exception as e:
            return e
        