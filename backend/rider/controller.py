from .manager import RiderManager
from trips.manager import TripsManager
class RiderController:
    @classmethod
    def book(cls,username,carId,location,destination,):
        """ Username , and users's location and destination. \n
        Location and destination to be a tuple of longitude and latitude"""
        TripsManager.createTrip(username,carId,location,destination)
    @classmethod
    def getRiderDetails(cls,username,):
        return RiderManager.riderDetails(username)
    
    @classmethod
    def registerRider(cls,username,email,password):
        """ Creates New Rider"""
        return RiderManager.registerRider(username,email,password)
    
    
    
        