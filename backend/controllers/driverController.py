from managers.managers import DriverManager,RiderManager
from .tripsController import TripsController
from strategies.cabMatchingStratergy import CabMatchingStratergy as Stratergy
class DriverContoller:
    class Priority:
        NORMAL="NORMAL"
        EMERGENCY='EMERGENCY'
    PROXIMITY_VALUE=0.1 #In km
    PROXIMITY_MAX=5
    EMERGENCY_MAX=15
    @classmethod
    def driverDetails(cls,carId):
      return DriverManager.getDriverDetails(carId)
    @classmethod
    def registerDriver(cls,username,email,password,carModel,carNumber,carId):
        """registers the car to the app"""
        return DriverManager.registerDriver(username,email,password,carModel,carNumber,carId)
    @classmethod
    def getDriver(cls,carId):
        return DriverManager.getDriver(carId)
    @classmethod
    def updateDriverLocation(cls,carId,location):
        """updates the driver location """
        DriverManager.updateDriverLocation(carId,location)
    @classmethod
    def updateDriverStatusandCurrentTrip(cls,driver,trip):
        DriverManager.updateDriverStatusandCurrentTrip(driver,trip)
    @classmethod
    def updateDriverOccupiedStatus(cls,carId,occupiedStatus):
        """Updates the occupied status/availability of the driver"""
        DriverManager.updateDriverOccupiedStatus(carId,occupiedStatus)

    @classmethod
    def endTrip(cls,driver):
        """It clears the driver current trip and updates the occupied status of the driver"""
        DriverManager.endTrip(driver)

    @classmethod
    def updateDriverOccupiedStatus(cls,carId,occupiedStatus):
        DriverManager.updateDriverOccupiedStatus(carId,occupiedStatus)
    
    @classmethod
    def clearDriverCurrentTrip(driver):
        DriverManager.clearDriverCurrentTrip(driver)

    @classmethod
    def getCars(cls,location,carType,priority=Priority.NORMAL):
        """returns the cars from the location within the geographical radius starting from 0.1 km to 5km"""
        # we can add the stratergy here
        proximityValue=DriverContoller.PROXIMITY_VALUE
        drivers=DriverManager.getCars(location,carType,proximityValue)
        print(f'At proximity {proximityValue} km, {len(drivers)} cars')
        maxdistance=DriverContoller.PROXIMITY_MAX
        if priority==DriverContoller.Priority.EMERGENCY:
            maxdistance=DriverContoller.EMERGENCY_MAX

        while not(drivers) and proximityValue <= maxdistance:
            proximityValue+=0.2 #if cannot find the drivers in this proximity, add 1 more km to the proximity
            drivers=DriverManager.getCars(location,carType,proximityValue)
            print(f'At proximity {proximityValue} km radius, {len(drivers)} cars')
        return drivers
    
    @classmethod
    def getCarsforBooking(cls,username,location,destination,carType,priority=Priority.NORMAL):
        rider=RiderManager.getRider(username)
        from rider.models import Rider
        assert isinstance(rider,Rider)
        if rider.currentTrip:
            return {'Error':'Rider has an ongoing trip, cannot search for cars','status':400},False
        drivers=DriverContoller.getCars(location,carType,priority)
        print("driver/controller/getCarsforBooking [GETTING] drivers",drivers)
        driver=Stratergy.matchCars(drivers)
        print("driver/controller/getCarsforBooking [MATCHING] drivers",driver)
        if driver:
            trip=TripsController.createTrip(rider,driver,location,destination)
            return trip,True
        return {'NA':'No ride is currently available','status':404},False #no driver found 
            
