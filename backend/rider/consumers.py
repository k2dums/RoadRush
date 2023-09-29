import json
from channels.generic.websocket import WebsocketConsumer
from enum import Enum
from controllers.controllers import DriverContoller,TripsController
from trips.models import Trips 
from clientChannel.models import RiderClientChannel,Rider,Driver,DriverClientChannel
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from common.request import RequestType 
import common.common as Common
from common.common import MessageType
class RiderStatus(Enum):
    """
    RIDING:the rider is intransit, enoroute to destination
    SEARCHING:looking for a driver
    COMPLETED:has completed his ride
    WAITING:waiting for the driver to arrive 
    NONE: just checking the app
    """
    RIDING='riding'
    SEARCHING='searching'
    COMPLETED='completed'
    WAITING='waiting'
    NONE='none'
    


class RiderConsumer(WebsocketConsumer):
    MAX_BOOK_TRIES=3
    def connect(self):
        self.rider_name=self.scope['url_route']['kwargs']['rider_name']
        self.rider_status=RiderStatus.NONE
        self.previousLocation=None
        self.priority=DriverContoller.Priority.NORMAL
        try:
            self.rider=Rider.objects.get(username=self.rider_name)
        except Exception:
            self.accept()
            self.send(text_data=json.dumps({'Error':"No such rider exists"}))
            self.close()
            print('Error: No such rider exists')
            return


        #the user will be taken  from django.contrib.auth
        riderChannel=RiderClientChannel.objects.filter(rider=self.rider)
        if riderChannel: #channel already exists, accept, send error, disconnect
            self.accept()
            self.send(text_data=json.dumps({'Error':'User logged in already from some other device'}))
            self.close()
            print('[RIDER] Error: User [RIDER] logged in already from some other device')
            return
        RiderClientChannel.objects.create(channel_name=self.channel_name,rider=self.rider)
        if not self.rider_status:
            self.rider_status=RiderStatus.NONE
        print('[RIDER] Connection request from RIDER:%s' % self.rider_name)
        self.accept()

    #need for a decorator to check if authenthicated
    def disconnect(self,close_code):
        RiderClientChannel.objects.filter(channel_name=self.channel_name).delete()
        print('[RIDER] Disconnected RIDER:%s' % self.rider_name)
    
    def receive(self, text_data):
        #limit the rate at which we are getting receive per 1 sec receive only 1 location ping 
        try:
            text_data_json=json.loads(text_data)
        except:
            self.send(json.dumps({"Error":'Data not in json format',"status":300}))
            return 
        #creating a action variable that sets the action
        print(f'Data sent by {self.rider_name}-{text_data}')
        
        request_type=text_data_json.get('type','NA').upper()

        if  request_type==RequestType.TripSearch: #if rider wants to search
            self.trip_search(text_data_json)
        elif  request_type==RequestType.TripBid:
            self.trip_bid(text_data_json)
        elif request_type==RequestType.TripCancel:
            self.trip_cancel(text_data_json)
        elif request_type==RequestType.TripTest:
            self.trip_test(text_data_json)
        elif request_type==RequestType.TripBidAccept:
            self.trip_bid_accept(text_data_json)
        else:
            self.send("Not a valid request Type was sent to the server")
            
        # if location and search:
        #     drivers=DriverContoller.getCars(location)
        #     if drivers:
        #         self.send(text_data={"search" :{"drivers":drivers,"status":'OK'}})
        #     else:# if no drivers:
        #         self.send(text_data={"search" :{"drivers":drivers,"status":'NA'}})
        # self.send(text_data={"search" :{"drivers":drivers,"status":'Invalid location'}})
        # #so after every x interval we send them drivers within a proximity
        # #what if we can't find the drivers (try till x sec then return null drivers)
        # #what if we are searching and we get pinged a locati        

#_____________________Helper Functions
    def trip_search(self,text_data_json):
            print('[RIDER] trip_search()')
            try:
                trip=text_data_json.get('message').get('trip')
            except:
                Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Check if the data is in format'})
                return
            location=trip.get('location')#will get location per 5sec interval
            destination=trip.get('destination')
            emergency=trip.get('emergency')
            self.carType=trip.get('carType')
            if emergency:
                self.priority=DriverContoller.Priority.EMERGENCY
            
            self.priority=DriverContoller.Priority.NORMAL
            if location and location.get('longitude') and  location.get('latitude'):
                if destination and destination.get('longitude') and destination.get('latitude'):
                    # tries=1
                    # while(tries<=RiderConsumer.MAX_BOOK_TRIES):
                    response,flag=DriverContoller.getCarsforBooking(self.rider_name,location,destination,self.carType)
                    if flag:
                        #if flag is true the response 
                        print(f"[SERVER] Data sent to the [user:{self.rider_name}],{response}")
                        response['status']=200
                        Common.selfSendMessg(self,MessageType.TRIP_REQUEST,response)
                    else:
                        #if flag is flase it returns a repsonse
                        print(f"[SERVER] Data sent to the [user:{self.rider_name}],{response}")
                        Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,response)
                        # break
                        # time.sleep(4000)
                        # tries+=1
                        # if tries>=RiderConsumer.MAX_BOOK_TRIES:
                        #     self.send(text_data=json.dumps({"book" :{"trip":None,"status":'NA'}}))
                else:#Invalid/Missing origin location
                    response={"Error":"Invalid Destination location",'status':400}
                    if not destination:
                        response={"Error":"Destination location not given",'status':400}
                        Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,response)
            else:#Invalid/Missing destination location
                response={"Error":'Invalid Origin location','status':400}
                if not location:
                    response={'Error':'Origin Location not given','status':400}
                Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,response)

    def trip_test(self,text_data_json):
            print('[RIDER] trip_test()')
            try:
                location=text_data_json['location']
                emergency=text_data_json.get('emergency')
                self.carType=text_data_json['carType']
                location=text_data_json['location']
                self.send(text_data=json.dumps({'Success':'Test query received successfully'}))
                self.send(text_data=json.dumps({"Sent by user":text_data_json}))
            except:
                self.send(text_data=json.dumps(
                    {'Error':'Check if data sent is in format'}
                ))
                return
            if not location:
                self.send(text_data=json.dumps({'error':'No location sent'}))
                return
          
            drivers=DriverContoller.getCars(location,self.carType)
            self.send(text_data=json.dumps({'drivers':[ driverSerialization(driver) for driver in drivers]}))
            return 
        
    def trip_cancel(self,text_data_json):
        print('[RIDER] trip_cancel()')
        flag,response=Common.trip_cancel(self,text_data_json)
        if not(flag):
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,response)
        else:
            if not(Common.sendDriverMessage(MessageType.TRIP_CANCEL_MESSAGE,response,text_data_json)):
                Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error sending message to the driverClient'})
            Common.selfSendMessg(self,MessageType.TRIP_CANCEL_MESSAGE,response)
        
    
    def trip_bid(self,text_data_json):
        print('[RIDER] trip_bid()')
        flag,response=Common.trip_bid(self,text_data_json)
        if not(flag):
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,response)
        else:
            try:
                if not(Common.sendDriverMessage(MessageType.BID_REQUEST,response,text_data_json)):
                    Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'error sending message to driverClient'})
                Common.selfSendMessg(self,MessageType.BID_REQUEST,{'request':f'Sending bid request of [{text_data_json["message"]["trip"]["bid_value"]}] for Trip {text_data_json["message"]["trip"]["id"]}'})
            except:
                Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Check if the data is in format '})
            
    
    def trip_bid_accept(self,text_data_json):
        print('[Driver] trip_bid_accept()')
        try:
            Common.sendRiderMessage(MessageType.FINAL,text_data_json['message'],text_data_json)
            Common.selfSendMessg(self,MessageType.FINAL,text_data_json['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'error sending final value'})

    #_______________EVENTS____________________________________
    def trip_data(self,event): #gets called only when trip is accepted by the driver
        print(f'Trip_data() call back function Rider Consumer ')
        print(event)
        try:
            rider=event['message']['trip']['rider']
            driver=event['message']['trip']['driver']
            origin=event['message']['trip']['origin']
            destination=event['message']['trip']['destination']
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'check format of the sent data trip_data '})
            return
        try:
           driver_obj=Driver.objects.get(username=driver['username'])
           rider_obj=Rider.objects.get(username=rider['username'])
        except:
            self.send(text_data=json.dumps({'Error':'Could not find the driver channel'}))
        try:
            tripData=TripsController.createTrip(rider_obj,driver_obj,origin,destination)
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':"Error creating trips"})
            return 
        try:
            if not(Common.sendDriverMessageObj(MessageType.TRIP_DATA,{"trip":tripData.serialize()},driver_obj)):
                Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error',"Error sending message to driverClientChannel"})
            Common.selfSendMessg(self,MessageType.TRIP_DATA,{"trip":tripData.serialize()})
        except:
            self.send(text_data=json.dumps({'Error':'Check the format of the data sent for trip_accept request'}))
            return 
            
        
    def bid_request(self,event): #rider receives bid request from the driver
        print(f'bid_request() call back function Rider Consumer')
        try:
            Common.selfSendMessg(self,MessageType.BID_REQUEST,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error when sending bid_request to the rider'})
    
    def bid_accept(self,event):
        print(f'bid_accept() call back function Rider Consumer')
        try:
            Common.selfSendMessg(self,MessageType.BID_REQUEST,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error when sending bid_accept to the rider'})

    def tripCancel_Message(self,event):
        print('trip_cancelMessage() call back funciton Rider consumer')
        try:
            Common.selfSendMessg(self,MessageType.TRIP_CANCEL_MESSAGE,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error when sending trip_cancelMessage to the rider'})

    def tripCompleted_Message(self,event):
        print('trip_endMessage() call back function Rider consumer')
        try:
            Common.selfSendMessg(self,MessageType.TRIP_END_MESSAGE,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error when sending trip_EndMessage to the rider'})

    def FINAL(self,event):
        print('final() call back function Rider consumer')
        try:
            Common.selfSendMessg(self,MessageType.FINAL,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error when sending trip_EndMessage to the rider'})

def driverSerialization(driver):
    return {
            'occupiedStatus':driver.occupiedStatus,
            'username':driver.username,
            'email':driver.email,
            'carId':driver.carId,
            'carNumber':driver.carNumber,
            'carModel':driver.carModel,
            'distance':str(driver.distance),
            'longitude':str(driver.location[0]),
            'latitude':str(driver.location[1]),
        }
        


   