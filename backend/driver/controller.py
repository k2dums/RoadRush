from .manager import DriverManager
from trips.manager import TripsManager
import time
class DriverContoller:
    PROXIMITY_MAX=5
    @classmethod
    def driverDetails(cls,carId):
      return DriverManager.getDriverDetails(carId)
    @classmethod
    def registerDriver(cls,username,email,password,carModel,carNumber,carId):
        """registers the car to the app"""
        return DriverManager.registerDriver(username,email,password,carModel,carNumber,carId)
        
    @classmethod
    def updateDriverLocation(cls,carId,location):
        """updates the driver location """
        DriverManager.updateDriverLocation(carId,location)

    @classmethod
    def updateDriverOccupiedStatus(cls,carId,occupiedStatus):
        """Updates the occupied status/availability of the driver"""
        DriverManager.updateDriverOccupiedStatus(carId,occupiedStatus)

    @classmethod
    def endTrip(cls,carId):
        TripsManager.endTrip(carId)

 
    @classmethod
    def getCars(cls,location,carType,proximityValue=0.1):
        """returns the cars from the location """
        # we can add the stratergy here
        drivers=DriverManager.getCars(location,carType,proximityValue)
        print(f'At proximity {proximityValue} km, {len(drivers)} cars')
        while not(drivers) and proximityValue <= DriverContoller.PROXIMITY_MAX:
            proximityValue+=0.2 #if cannot find the drivers in this proximity, add 1 more km to the proximity
            drivers=DriverManager.getCars(location,carType,proximityValue)
            print(f'At proximity {proximityValue} km radius, {len(drivers)} cars')
        return drivers,proximityValue
        # drivers=DriverManager.getCars(location,proximityValue)
        # return drivers,proximityValue
            
    

