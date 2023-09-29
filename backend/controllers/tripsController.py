from managers.tripsManager import TripsManager,RiderManager,DriverManager

class TripsController:
    @classmethod
    def updateTripStatus(cls,trip,action):
        return TripsManager.updateTripStatus(trip,action)
    @classmethod
    def getTrip(cls,tripId):
        return TripsManager.getTrip(tripId)
    @classmethod
    def createTrip(cls,rider,driver,origin,destination):
        return TripsManager.createTrip(rider,driver,origin,destination)
    # @classmethod
    # def createTrip_riderUsername(cls,username,carId,origin,destination):
    #     return TripsManager.createTrip_riderUsername(username,carId,origin,destination)
    @classmethod
    def endTrip(cls,carId,username):
        return TripsManager.endTrip(carId,username)
    @classmethod
    def cancelTrip(cls,carId,username):
        return TripsManager.cancelTrip(carId,username,)
    @classmethod
    def endTrip_byObjects(cls,riderObj,driverObj,tripObj):
        return TripsManager.endTrip_byObjects(riderObj,driverObj,tripObj)
    @classmethod
    def cancelTrip_byObjects(cls,riderObj,driverObj,tripObj):
        return TripsManager.cancelTrip_byObjects(riderObj,driverObj,tripObj)
    @classmethod
    def check_TripIntegrity(cls,riderObj,driverObj):
        return TripsManager.check_TripIntegrity(riderObj,driverObj)