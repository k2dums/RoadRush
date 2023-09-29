
import json
from controllers.controllers import TripsController
from rider.models import Rider
from driver.models import Driver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from clientChannel.models import RiderClientChannel,DriverClientChannel


class MessageType:
     ERROR_MESSAGE='error_message'
     TRIP_CANCEL_MESSAGE='tripCancel_Message'
     TRIP_END_MESSAGE='tripCompleted_Message'
     BID_REQUEST='bid_request'
     TRIP_DATA='trip_data'
     BID_ACCEPT='bid_accept'
     TRIP_REQUEST='trip_request'
     NEAR_BY_DRIVERS='near_by_drivers'
     FINAL='FINAL'

def checkTripDataFormat(tripData):
        assert isinstance(tripData,dict)
        try:
            if not(tripData['rider']):
                return {'Error':"rider section is missing"}
            if not(tripData['rider'].has_key('username')) or not (tripData['rider'].has_key('id')):
                return {'Error':'rider section has missing data'}
            if not(tripData['origin']) or not(tripData['destination']):
                return {'Error':'Either origin or desitinaton location is not given'}
            if not(tripData['origin'].has_key('longitude'))  or  not(tripData['origin'].has_key('latitude')):
                return {'Error':'Origin location has missing data'}
            if not(tripData['destination'].has_key('longitude'))  or  not(tripData['destination'].has_key('latitude')):
                return {'Error':'Destination location has missing data'}
            if not(tripData['rider'].has_key('id')) or not(tripData['rider'].has_key('username')):
                return {'Error':'rider section has missing data'}
        except:
            return {'Error':'TripData not in correct format'}

def trip_end(self,text_data_json):
        
        # response=checkTripDataFormat(tripData)
        # if response:
        #     print(response)
        #     self.send(text_data=json.dumps(response))
        #     return 
        try:
              trip=text_data_json.get('message').get('trip')
        except:
             print({'Error':'Check format of the data. Check if trip section exists'})
             return False,{'Error':'Check format of the data. Check if trip section exists'}
        
        try:
            rider_username=trip['rider']['username']
        except:
            print({'Error':'Error when fetching rider details from trip data'})
            return False,{'Error':'Error when fetching rider details from trip data'}
        try:
            riderObj=Rider.objects.get(username=rider_username)
        except:
            print({'Error':'error when fetching rider object from database'})
            return False,{'Error':'error when fetching rider object from database'}
        try:
             driverObj=Driver.objects.get(username=self.driver_username)
        except:
            print({'Error':'error when fetching driver object from database'})
            return False,{'Error':'error when fetching driver object from database'}
             
        response=TripsController.check_TripIntegrity(riderObj,driverObj)
        if response:
            return False,response
        tripObj=driverObj.currentTrip
        flag,response=TripsController.endTrip_byObjects(riderObj,driverObj,tripObj)
        return flag,response
  
        
        
        
def trip_cancel(self,text_data_json):
        try:
              trip=text_data_json.get('message').get('trip')
        except:
             print({'Error':'Check format of the data. Check if trip section exists'})
             return False,{'Error':'Check format of the data. Check if trip section exists'}
        # response=checkTripDataFormat(tripData)
        # if response:
        #     print(response)
        #     self.send(text_data=json.dumps(response))
        #     return 
        try:
            rider_username=trip['rider']['username']
        except:
            print({'Error':'Error when fetching rider details from trip data'})
            return False,{'Error':'Error when fetching rider details from trip data'}
        try:
            riderObj=Rider.objects.get(username=rider_username)
        except:
            print({'Error':'error when fetching rider object from database'})
            return False,{'Error':'Error when fetching rider object from database'}
        try:
             driver_username=trip['driver']['username']
             driverObj=Driver.objects.get(username=driver_username)
        except:
             print({'Error':'error when fetching driver object from database'})
             return False,{'Error':'error when fetching driver object from database'}
             
        response=TripsController.check_TripIntegrity(riderObj,driverObj)
        if response:#if there is a response from check_TripIntegrity() means error send it to the client
            return False,response
        tripObj=driverObj.currentTrip
        flag,response=TripsController.cancelTrip_byObjects(riderObj,driverObj,tripObj)
        return flag,response #can't send to rider or driver channel specifically as this function is common to both rider and client


def trip_bid(self,text_data_json):
        try:
              trip=text_data_json.get('message').get('trip')
        except:
             print({'Error':'Check format of the data. Check if trip section exists'})
             return False,{'Error':'Check format of the data. Check if trip section exists'}
        # response=checkTripDataFormat(trip)
        # if response:
        #     self.send(text_data=json.dumps(response))
        #     return
        try:
            bid_value=trip['bid_value']
        except:
            #  selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'bid_value is missing'})
             return False,{'Error':'bid_value is missing'}
        try:
            if not(isinstance(bid_value,int)):
                # selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Bid value not an integer for request type bid_request'})
                return False,{'Error':'Bid value not an integer for request type bid_request'}
        except:
            # selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'bid_value Value Error. Check if integer'})
            return False,{'Error':'bid_value Value Error. Check if integer'}
        # try:
        #     selfSendMessg(self,MessageType.BID_REQUEST,"Sending bid request") #sending to the sender that bid is being sent
        # except:
        #     #  selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error sending bid request message'})
        #      return False,{'Error':'Error sending bid request message'}
        
        try:
            return True,{"trip":{
                            'id':trip['id'],
                            'bid_value':bid_value
                            }
                    }
        except:
             return False, {'Error':'Error sendin the bid request.Check if data in format'}
        

def sendRiderMessage(messg_type,message,text_data_json):
    channel_layer=get_channel_layer()
    try:
        rider_Obj=Rider.objects.get(username=text_data_json['message']['trip']['rider']['username'])
        rider_clientChannel=RiderClientChannel.objects.get(rider=rider_Obj)
        async_to_sync(channel_layer.send)(rider_clientChannel.channel_name,{
            "type":messg_type,
            "message":message
        })
        return True
    except:
         return False

def sendRiderMessageObj(messg_type,message,riderObj):
    channel_layer=get_channel_layer()
    try:
        rider_clientChannel=RiderClientChannel.objects.get(rider=riderObj)
        async_to_sync(channel_layer.send)(rider_clientChannel.channel_name,{
            "type":messg_type,
            "message":message
        })
        return True
    except:
         return False
    
def sendDriverMessage(messg_type,message,text_data_json):
    channel_layer=get_channel_layer()
    try:
        driverObj=Driver.objects.get(username=text_data_json['message']['trip']['driver']['username'])
        driver_clientChannel=DriverClientChannel.objects.get(driver=driverObj)
        async_to_sync(channel_layer.send)(driver_clientChannel.channel_name,{
            "type":messg_type,
            "message":message
        })
        return True
    except:
         return False
    
def sendDriverMessageObj(messg_type,message,driver_obj):
     channel_layer=get_channel_layer()
     try:
        driver_clientChannel=DriverClientChannel.objects.get(driver=driver_obj)
        async_to_sync(channel_layer.send)(driver_clientChannel.channel_name,{
            "type":messg_type,
            "message":message
        })
        return True
     except:
        return False
     

def selfSendMessg(self,messg_type,messg):
     try:
          self.send(text_data=json.dumps(
               {
                    'type':messg_type,
                    'message':messg
               }
          ))
     except:
          self.send(text_data=json.dumps(
               {'Error':'error sending message '}
          ))