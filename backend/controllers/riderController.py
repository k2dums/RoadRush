from managers.managers import RiderManager,DriverManager
from .tripsController import TripsController
class RiderController:
    @classmethod
    def setRiderTrip(cls,rider,trip):
        RiderManager.setRiderTrip(rider,trip)
    @classmethod
    def getRider(cls,username):
        return RiderManager.getRider(username)
    @classmethod
    def book(cls,username,carId,location,destination,):
        """ Username , and users's location and destination. \n
        Location and destination to be a tuple of longitude and latitude"""
        rider=RiderManager.getRider(username)
        driver=DriverManager.getDriver(carId)
        TripsController.createTrip(rider,driver,location,destination)
    @classmethod
    def getRiderDetails(cls,username,):
        return RiderManager.riderDetails(username)
    
    @classmethod
    def registerRider(cls,username,email,password):
        """ Creates New Rider"""
        return RiderManager.registerRider(username,email,password)
    
    @classmethod
    def endTrip(rider):
        """It clears the run current trip and updates the onTrip status of the rider"""
        RiderManager.endTrip(rider)