from managers.managers import RiderManager,DriverManager
# from stratergies.cabMatchingStratergy import CabMatchingStratergy
# from stratergies.pricingStratergy import PricingStratergy
from trips.models import Trips
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import fromstr
from rider.models import Rider
from driver.models import Driver
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
    def cancelTrip(cls,carId,username):
        try:
            driver=DriverManager.getDriver(carId)
            rider=RiderManager.gerRider(username)
        except:
            return False,{'Error':'Invalid/Missing carId or username'}
        response=TripsManager.check_TripIntegrity(rider,driver)
        if response:
            return False,response
        trip=driver.currentTrip
        
        return TripsManager.cancelTrip_byObjects(rider,driver,trip)
        
    
    @classmethod
    def endTrip(cls,carId,username):
        """Ends the trip of the car, a trip ends only if it is cancelled or endtrip"""
        try:
            driver=DriverManager.getDriver(carId)
            rider=RiderManager.getRider(username)
        except:
            return False,{"Error":'Invalid/Missing carId or username'}
        response=TripsManager.check_TripIntegrity(rider,driver)
        if response:
            return False,response
        trip=driver.currentTrip
        return TripsManager.endTrip_byObjects(rider,driver,trip)
        
    @classmethod
    def endTrip_byObjects(cls,riderObj,driverObj,trip_obj):  
        try:
            response=TripsManager.updateTripStatus(trip_obj,Trips.Trip_Status.COMPLETED)
            if not response:
                return False,{"Error":"Action not allowed for the trip completion/ending"}
        except:
            return False,{"Error":"Ending/Completion of the trip incurred a error"}
        
        try:
            DriverManager.endTrip(driverObj)
            RiderManager.endTrip(riderObj)
        except:
            return False,{"Error":"Updating the status of the driver/rider incurred a error while ending/completion"}
        
        return True,f"Successfully completed the trip {trip_obj.id}"
    
    @classmethod
    def cancelTrip_byObjects(cls,riderObj,driverObj,trip_Obj):
      
        try:
            response=TripsManager.updateTripStatus(trip_Obj,Trips.Trip_Status.CANCELLED) 
            if not(response):
                return False,{'Error':'Action is not allowed for the trip cancellation'}
        except:
            return False,{'Error':'Cancelling the trip incurred a error'}
        try:
            DriverManager.endTrip(driverObj)
            RiderManager.endTrip(riderObj)
        except:
            return False,{"Error":"Updating the status of the driver/rider incurred a error when cancelling"}
        return True,f"Successfully cancelled the trip {trip_Obj.id}"
    
    @classmethod
    def check_TripIntegrity(cls,riderObj,driverObj):
        try:
            assert isinstance(riderObj,Rider)
            assert isinstance(driverObj,Driver)
        except:
            return {'Error':'Not of type Rider/Driver'}
        try:
            trip=driverObj.currentTrip
            riderTrip=riderObj.currentTrip
        except:
            return {'Error':'Rider/Driver doesn\'t have attribute currentTrip'}
        if not(trip) or not(riderTrip):
            return{
                "Error":"Driver/Rider has no currentTrips"
            }
        # The id of these trip and riderTrip are different as they are attributes of their respective models and thus not pointing to same object
        if not (trip == riderTrip) :
            return {
                'Error':"Integrity Error, rider and driver points to different trip"
            }
        try:
            assert isinstance(trip,Trips)
        except:
            return {'Error':'trip is not of type Trip'}

