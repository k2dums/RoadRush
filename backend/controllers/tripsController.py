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
    def endTrip(cls,carId,username,action):
        return TripsManager.endTrip(carId,username,action)