from channels.generic.websocket import WebsocketConsumer
import json
from controllers.controllers import DriverContoller
from clientChannel.models import DriverClientChannel,Driver,RiderClientChannel,Rider
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
class RequestType:
    TripAccept="TRIP_ACCEPT"
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
        text_data_json=json.loads(text_data)
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
        trip=text_data_json.get('trip',None)
        rider=trip.get('rider',None)
        origin=trip.get('origin',None)
        destination=trip.get('destination',None)
        if request_type==RequestType.TripAccept:
            self.trip_accept(rider,origin,destination)
            

    

    def trip_accept(self,rider,origin,destination):
        driver_username=self.driver_username
        rider_channel=None
        try:
            rider_obj=Rider.objects.get(username=rider['username'])
            rider_channel=RiderClientChannel.objects.get(rider=rider_obj)
        except:
            self.send(text_data=json.dumps({'Error':'Returned more than one user for the RiderClientChannel'}))
            return
        channel_layer = get_channel_layer()
        channel_layer=get_channel_layer()
        async_to_sync(channel_layer.send)(rider_channel.channel_name,{
                                "type":"trip_accept",
                                'origin':{
                                          'longitude':origin['longitude'],
                                          'latitude':origin['latitude']
                                          },
                                'destination':{
                                          'longitude':destination['longitude'],
                                          'latitude':destination['latitude']
                                          },
                                'rider':{
                                    'id':rider['id'],
                                    'username':rider['username']
                                },
                                'driver':{
                                    'username':driver_username,
                                }

            })
        print(f'Sending Trip_Accept to user {rider["username"]} ')

#____________________EVENTS___________________________    
    def trip_request(self,event):
        print(f'Trip_request() call back function \n {event} ')
        self.send(text_data=json.dumps({'type':'trip_request', #trip request is only sent to drivers
                                        'trip':{
                                            'origin':event['origin'],
                                            'destination':event['destination'],
                                            'rider':{
                                                'username':event['rider_username'],
                                                'id':event['rider_id']
                                            }
                                        }
                                        }))
 