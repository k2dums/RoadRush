from driver.manager import DriverManager
from rider.manager import RiderManager
from stratergies.cabMatchingStratergy import CabMatchingStratergy
from stratergies.pricingStratergy import PricingStratergy

class TripsManager:
    @classmethod
    def createTrip(cls,username,carId,location,destination):
        """Creates trip based on the the username and carId"""
        pass

    def endTrip(cls,carId):
        """Ends the trip of the car"""
        car=DriverManager.getDriver(carId)
        DriverManager.updateDriverAvailability(carId,False)


