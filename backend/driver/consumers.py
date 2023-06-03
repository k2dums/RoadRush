from channels.generic.websocket import WebsocketConsumer
import json
from driver.controller import DriverContoller
class DriverConsumer(WebsocketConsumer):
    def connect(self):
        self.carId=self.scope['url_route']['kwargs']['driver_id']
        print('[Driver] Connection Request DRIVER:%s' % self.driver_id)
        self.accept()
    def disconnect(self,close_code):
        print('[Driver] Disconnected DRIVER:%s' % self.driver_id)
        pass
    def receive(self, text_data):
        text_data_json=json.loads(text_data)
        location=text_data_json.get('location')
        DriverContoller.updateDriverLocation(location)
        bookingRequest=text_data_json.get('bookingRequest')
        if bookingRequest:
            self.send(text_data=bookingRequest)
        # The driver continuously pings the server of its location
        # if the driver hasn't pinged once in the last 4 sec it is removed
        # use of R-Tree for geo spatial queries
