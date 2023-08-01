from channels.generic.websocket import WebsocketConsumer
import json
from controllers.controllers import DriverContoller
from clientChannel.models import DriverClientChannel,Driver
class DriverConsumer(WebsocketConsumer):
    def connect(self):
        self.driverId=self.scope['url_route']['kwargs']['driver_id']
        #getting the driver obj based on django.contrib.auth
        try:
            self.driver=Driver.objects.get(id=self.driverId)
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
        print('[Driver] Connection Request DRIVER:%s' % self.driverId)
        self.accept()

        
    def disconnect(self,close_code):
        DriverClientChannel.objects.filter(channel_name=self.channel_name).delete()
        print('[Driver] Disconnected DRIVER:%s' % self.driverId)
        pass
    def receive(self, text_data):
        text_data_json=json.loads(text_data)
        print(f'{[self.driver.username]} Message received :{text_data}')
        # location=text_data_json.get('location')
        # DriverContoller.updateDriverLocation(location)
        # bookingRequest=text_data_json.get('bookingRequest')
        # if bookingRequest:
        #     self.send(text_data=bookingRequest)
        # The driver continuously pings the server of its location
        # if the driver hasn't pinged once in the last 4 sec it is removed
        # use of R-Tree for geo spatial queries
    
    def trip_request(self,event):
        print(f'Trip_request() call back function \n {event} ')
        self.send(text_data=json.dumps({'type':'trip_request', #trip request is only sent to drivers
                                        'trip':{
                                            'origin':event['origin'],
                                            'destination':event['destination'],
                                            'rider':{
                                                'name':event['rider_username'],
                                                'id':event['rider_id']
                                            }
                                        }
                                        }))
    