
from driver.models import Driver
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance 
from authentication.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json
class DriverManager:
    """carId needs to be unique
    """
    @classmethod 
    def registerDriver(cls,username,email,password,carModel,carNumber,carId):
        if Driver.objects.filter(username=username):
           return {'error':'username already exists'}
        if Driver.objects.filter(email=email):
           return {'error':'email already exists'}
        if not(email):
            return {'error':'email is empty'}
        if not(username):
            return {'error':'username is empty'}
        if not(password):
            return {'error':'password is empty'}
        if not(carModel):
            return {'error':'carModel is empty'}
        if not(carNumber):
            return {'error':'carNumber is empty'}
        if not(carId):
            return {'error':'carId is empty'}
        if len(password)<6:
            return {'error':'password length less than 6'}
        try:
            validate_email(email)
        except ValidationError:
            return {'error':'email not valid'}
        
        try:
           driver=Driver.objects.create_user(username=username,email=email,password=password,carModel=carModel,carNumber=carNumber,carId=carId)
           return driver
        except Exception as e:
            print('error',e)
            return e

     
    @classmethod
    def getDriverDetails(cls,carId):
        """Returns the driver details"""
        driver=Driver.objects.get(carId=carId)
        assert isinstance(driver,Driver)
        return {
            'username':driver.username,
            'email':driver.email,
            'carId':driver.carId,
            'carModel':driver.carModel,
            'carNumber':driver.carNumber,
            'carLocation':{'longitude':driver.location.x,
                           'latitude':driver.location.y
                           },
            'occupiedStatus':driver.occupiedStatus,
        }
    
    @classmethod
    def getDriver(cls,carId):
        """Returns the driver object"""
        driverObj=Driver.objects.get(carId=carId)
        assert isinstance(driverObj,Driver)
        return driverObj
    
    @classmethod
    def updateDriverLocation(cls,carId,location):
        """
        location as a tuple
        """
        longitude=location['longitude']
        latitude=location['latitude']
        driver=Driver.objects.get(carId=carId)
        assert isinstance(driver,Driver)
        driver.location=Point(longitude,latitude,srid=4326)
        driver.save()

    @classmethod
    def updateDriverOccupiedStatus(cls,carId,occupiedStatus):
        """Updates the availabilty of the driver:Boolean """
        driver=Driver.objects.get(carId=carId)
        assert isinstance(driver,Driver)
        driver.occupiedStatus=occupiedStatus
        driver.save()
        
    @classmethod
    def getCars(cls,location,ProximityValue):
        """Returns all the cabs withtin the promity value from the location"""
        longitude=location['longitude']
        latitude=location['latitude']

        userLocation=Point(float(longitude),float(latitude),srid=4236)

        drivers=Driver.objects.filter(location__distance_lt=(userLocation, Distance(km=ProximityValue)))
        return drivers
      

        


