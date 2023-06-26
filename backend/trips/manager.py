from driver.manager import DriverManager
from rider.manager import RiderManager
# from stratergies.cabMatchingStratergy import CabMatchingStratergy
# from stratergies.pricingStratergy import PricingStratergy
from .models import Trips
class TripsManager:
    @classmethod
    def createTrip(cls,username,carId,origin,destination):
        """Creates trip based on the the username and carId"""
        driver=DriverManager.getDriver(carId)
        rider=RiderManager.getRider(username)
        trip=Trips(rider=rider,driver=driver,origin=origin,destination=destination,status=Trips.Trip_Status.BOOKED)
        DriverManager.updateDriverOccupiedStatus_driverObj(driver,True)
        trip.save()

    def endTrip(cls,carId):
        """Ends the trip of the car"""
        DriverManager.updateDriverOccupiedStatus(carId,False)


