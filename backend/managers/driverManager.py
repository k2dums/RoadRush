
from driver.models import Driver
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
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
    def updateDriverOccupiedStatus_driverObj(cls,driver,occupiedStatus):
        """Updates the availabilty of the driver:Boolean """
        assert isinstance(driver,Driver)
        driver.occupiedStatus=occupiedStatus
        driver.save()
    
    @classmethod
    def updateDriverStatusandCurrentTrip(cls,driver,trip):
        """Status of driver will be occupied and current trip will be set"""
        assert isinstance(driver,Driver)
        driver.occupiedStatus=True
        driver.currentTrip=trip
        driver.save()
        
    @classmethod
    def getCars(cls,_location,carType,ProximityValue):
        """Returns all the cabs withtin the promity value from the location"""
        longitude=_location['longitude']
        latitude=_location['latitude']
        # ProximityValue=ProximityValue*1000
        userLocation=Point(float(longitude),float(latitude),srid=4236)

        if not(carType) or carType.upper==None:
            drivers=Driver.objects.filter(location__distance_lte=(userLocation, D(km=ProximityValue))).annotate(distance=Distance('location',userLocation)).order_by('distance') 
            return drivers 
        drivers=Driver.objects.filter(location__distance_lte=(userLocation, D(km=ProximityValue)),carType=carType.upper()).annotate(distance=Distance('location',userLocation)).order_by('distance')        
        return drivers
      

    @classmethod
    def clearDriverCurrentTrip(cls,driver):
        """Parameter is a driver object that clears the driver trip"""
        assert isinstance(driver,Driver)
        driver.save()

    @classmethod
    def updateDriverOccupiedStatus(cls,driver,occupiedStatus):
        """Updates the availabilty of the driver:Boolean """
        assert isinstance(driver,Driver)
        driver.occupiedStatus=occupiedStatus
        driver.save()

    @classmethod
    def endTrip(cls,driver):
        driver.currentTrip=None
        driver.occupiedStatus=False
        driver.save()
