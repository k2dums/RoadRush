from channels.generic.websocket import WebsocketConsumer
import json
from controllers.controllers import DriverContoller,TripsController
from clientChannel.models import DriverClientChannel,Driver,RiderClientChannel,Rider
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from common.request import RequestType
import common.common as Common
from common.common import MessageType
class DriverConsumer(WebsocketConsumer):
    
    def connect(self):
        self.driver_username=self.scope['url_route']['kwargs']['driver_username']
        #getting the driver obj based on django.contrib.auth
        try:
            self.driver=Driver.objects.get(username=self.driver_username)
        except:
            self.accept()
            self.send(text_data=json.dumps({'Error':"No such driver exists"}))
            self.close()
            print('Error: No such driver exists')
            return
        
        #driver will be taken from django.contrib.auth
        driverChannel=DriverClientChannel.objects.filter(driver=self.driver)
        if driverChannel:#channel already exists, accept, send error and dc
            self.accept()
            self.send(text_data=json.dumps({'Error':'User logged in already from some other device'}))
            self.close()
            print('Error:User [DRIVER] logged in already from some other device')
            return 
        
        DriverClientChannel.objects.create(channel_name=self.channel_name,driver=self.driver)
        print('[Driver] Connection Request DRIVER:%s' % self.driver_username)
        self.accept()

        
    def disconnect(self,close_code):
        DriverClientChannel.objects.filter(channel_name=self.channel_name).delete()
        print('[Driver] Disconnected DRIVER:%s' % self.driver_username)
        pass
    def receive(self, text_data):
        try:
            text_data_json=json.loads(text_data)
        except:
            self.send(json.dumps({"Error":'Data not in json format',"status":300}))
            return 
        print(f'[DRIVER]{self.driver.username} Message received :{text_data}')
        # location=text_data_json.get('location')
        # DriverContoller.updateDriverLocation(location)
        # bookingRequest=text_data_json.get('bookingRequest')
        # if bookingRequest:
        #     self.send(text_data=bookingRequest)
        # The driver continuously pings the server of its location
        # if the driver hasn't pinged once in the last 4 sec it is removed
        # use of R-Tree for geo spatial queries
        request_type=text_data_json.get('type','NA').upper() # done purposely for checking as if None type can't be uppercased
        if request_type==RequestType.TripAccept:
            self.trip_accept(text_data_json)
            return
        elif request_type==RequestType.TripCancel:
            self.trip_cancel(text_data_json)
            return 
        elif request_type==RequestType.TripEnd:
            self.trip_end(text_data_json)
            return 
        elif request_type==RequestType.TripBid:
            self.trip_bid(text_data_json)
        elif request_type==RequestType.TripBidAccept:
            self.trip_bid_accept(text_data_json)
        else:
            self.send(text_data=json.dumps( 'Not a valid request type')
               
            )

#_______________________ Helper Functions

    def trip_accept(self,text_data_json):
        print('[Driver] trip_accept()')
        driver_username=self.driver_username
        # response=Common.checkTripDataFormat(tripData)
        # if response:
        #     print(response)
        #     self.send(text_data=json.dumps(response))
        #     return 
        try: #check if the values are valid
            tripData=text_data_json.get('message').get('trip')
            tripData['origin']
            tripData['destination']
            rider=tripData['rider']
        except:
            print({'Error':'Error when extracting data from Trip Data'})
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Check format of the sent data'})
            return 
        try:
            rider_obj=Rider.objects.get(username=rider['username'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'error getting the rider object'})
            return
        tripData['driver']={'username':driver_username}
        if not(Common.sendRiderMessageObj(MessageType.TRIP_DATA,{'trip':tripData},rider_obj)): #if returns error means error
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error',"error sending the trip_accept request to the riderClientChannel"})
            return
        print(f'Sending Trip_Accept to user {rider["username"]} ')

    def trip_end(self,text_data_json):
        print('[Driver] trip_end()')
        flag,response=Common.trip_end(self,text_data_json)
        if not(flag):#if flag is false, ie error and send it to the client
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,response)
            return 
        else: #if true meaning the operation was succesful and send also to the riderClient
           if not (Common.sendRiderMessage(MessageType.TRIP_END_MESSAGE,response,text_data_json)):#if returns error means error
               Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'error sending message to riderClientChannel'})
           Common.selfSendMessg(self,MessageType.TRIP_END_MESSAGE,response)
        
    def trip_cancel(self,text_data_json):
        print('[Driver] trip_cancel()')
        flag,response=Common.trip_cancel(self,text_data_json)
        if not(flag):#if flag is false means error send only to the client itself 
            Common.selfSendMessg(self,Common.MessageType.ERROR_MESSAGE,response)
            return 
        else: #if true meaning the operation was succesful and send also to the riderClient
            if not (Common.sendRiderMessage(Common.MessageType.TRIP_CANCEL_MESSAGE,response,text_data_json)):
                Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'error sending message to riderClientChannel'})
            Common.selfSendMessg(self,MessageType.TRIP_CANCEL_MESSAGE,response)

    def trip_bid(self,text_data_json):
        print('[Driver] trip_bid()')
        flag,response=Common.trip_bid(self,text_data_json)
        if not(flag):
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,response)
        else:
            try:
                if not(Common.sendRiderMessage(MessageType.BID_REQUEST,response,text_data_json)):
                    Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'error sending message to riderClient'})
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

#____________________EVENTS___________________________    
    def trip_request(self,event):
        print(f'trip_request() call back function Driver Consumer')
        print(event['message'])
        try:
            Common.selfSendMessg(self,MessageType.TRIP_REQUEST,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{ 'Error':'Error when sending trip_request to the Driver'})

    def trip_data(self,event):
        print(f'trip_data() call back function Driver Consumer ')
        try:
            Common.selfSendMessg(self,MessageType.TRIP_DATA,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{ 'Error':'Error when sending trip_data to the Driver'})

    def bid_request(self,event): #driver receives bid request from the rider
        print(f'bid_request() call back function Driver Consumer')
        try:
            Common.selfSendMessg(self,MessageType.BID_REQUEST,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error when sending bid_request to the Driver'})
    def bid_accept(self,event):
        print(f'bid_accept() call back functoin Driver Consumer')
        try:
            Common.selfSendMessg(self,MessageType.BID_ACCEPT,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error when sending bid_accept to the Driver'})
    def tripCancel_Message(self,event):
        print(f'trip_cancelMessg() call back function Driver Consumer')
        try:
            Common.selfSendMessg(self,MessageType.TRIP_CANCEL_MESSAGE,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error when sending tripCancel message to the Driver'})
    
    def FINAL(self,event):
        print('final() call back function Driver consumer')
        try:
            Common.selfSendMessg(self,MessageType.FINAL,event['message'])
        except:
            Common.selfSendMessg(self,MessageType.ERROR_MESSAGE,{'Error':'Error when sending trip_EndMessage to the rider'})
    

#Action similar in both rider and driver
#action_cancelTrip === trip_cancel
#trip_bid === trip_bid
#trip_end === action_endTrip
#checkTripFormat needed in both rider and driver