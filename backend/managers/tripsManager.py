from managers.managers import RiderManager,DriverManager
# from stratergies.cabMatchingStratergy import CabMatchingStratergy
# from stratergies.pricingStratergy import PricingStratergy
from trips.models import Trips
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import fromstr
class TripsManager:
    allowed_status=[Trips.Trip_Status.BOOKED,Trips.Trip_Status.CANCELLED,Trips.Trip_Status.COMPLETED,Trips.Trip_Status.ONGOING,Trips.Trip_Status.NA]

    @classmethod
    def updateTripStatus(cls,trip,action):
        """Parameter is trip object and status"""
        assert isinstance(trip,Trips)
        if action in TripsManager.allowed_status:
            trip.status=action
            trip.save()
            return True
        return False #returns False only when action is not valid
    
    @classmethod
    def getTrip(tripId):
        trip=Trips.objects.get(id=tripId)
        return trip
    @classmethod
    def createTrip(cls,rider,driver,origin,destination):
        """Creates trip based on the the username and carId"""
        # driver=DriverManager.getDriver(carId)
        origin_longitude=origin['longitude']
        origin_latitude=origin['latitude']
        origin=fromstr(f'POINT({origin_longitude} {origin_latitude})', srid=4326)
        destination_longitude=destination['longitude']
        destination_latitude=destination['latitude']
        destination=fromstr(f'POINT({destination_longitude} {destination_latitude})', srid=4326)
        trip=Trips(rider=rider,driver=driver,origin=origin,destination=destination,status=Trips.Trip_Status.BOOKED)
        trip.save()
        RiderManager.setRiderTrip(rider,trip)
        DriverManager.updateDriverStatusandCurrentTrip(driver,trip)
        return trip
    
    # def createTrip_riderUsername(cls,username,carId,origin,destination):
    #     """Creates trip based on username and carId, origin and destination"""
    #     rider=RiderManager.getRider(username)
    #     return TripsManager.createTrip_riderObj(rider,carId,origin,destination)

    @classmethod
    def endTrip(cls,carId,username,action):
        """Ends the trip of the car, a trip ends only if it is cancelled or endtrip"""
        try:
            driver=DriverManager.getDriver(carId)
            rider=RiderManager.getRider(username)
        except:
            return {"Error":'Invalid/Missing carI or username'}
        trip=driver.currentTrip
        riderTrip=rider.currentTrip

        print('Driver trip:',trip)
        print('Rider trip',riderTrip)
        if not(trip) or not(riderTrip):
            return{
                "Error":"Driver/Rider has no currentTrips"
            }
        # The id of these trip and riderTrip are different as they are attributes of their respective models and thus not pointing to same object
        if not (trip == riderTrip) :
            return {
                'Error':"Integrity Error, rider and driver points to different trip"
            }
       
        assert isinstance(trip,Trips)

        if not(action.upper() in [Trips.Trip_Status.CANCELLED,Trips.Trip_Status.COMPLETED]):
            return {"Error":"Invalid action (action is not an allowed action)"}
        try:
            response=TripsManager.updateTripStatus(trip,action.upper())
            print("Response",response)
            if not response:
                return {"Error":"Invalid action (action is not an allowed action)"}
        except:
            return {"Error":"Invalid input for action"}
        
        try:
            DriverManager.endTrip(driver)
            RiderManager.endTrip(rider)
        except:
            return {"Error":"Error when updating and ending trip"}
        
        return f"Successfully ended the trip {trip.id}"
        


