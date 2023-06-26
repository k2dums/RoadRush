import json
from channels.generic.websocket import WebsocketConsumer
from enum import Enum
from driver.controller import DriverContoller
import time
from trips.manager import TripsManager
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
    MAX_BOOK_TRIES=5
    def connect(self):
        self.rider_name=self.scope['url_route']['kwargs']['rider_name']
        self.rider_status=RiderStatus.NONE
        self.previousLocation=None
        self.proximityValue=0.1
        if not self.rider_status:
            self.rider_status=RiderStatus.NONE
        print('Connection request from RIDER:%s' % self.rider_name)
        self.accept()
        

    def disconnect(self,close_code):
        print('[RIDER] Disconnected RIDER:%s' % self.rider_name)
    
  
    def receive(self, text_data):
        #limit the rate at which we are getting receive per 1 sec receive only 1 location ping 
        text_data_json=json.loads(text_data)
        search=text_data_json.get('search')
        book=text_data_json.get('book')
        newSearch=text_data_json.get('newSearch')
        self.carType=text_data_json.get('carType')
        # print('Closeby drivers',len(drivers))
        # print('Proxitmity Value',self.proximityValue)
        print(f'Data sent by {self.rider_name}-{text_data}')
        if newSearch: #resets the promityValue for scan to 1km 
             self.proximityValue=0.1
        if (search):
            location=text_data_json.get('location')#will get location per 5sec interval
            drivers,self.proximityValue=DriverContoller.getCars(location,self.carType,self.proximityValue)
            self.send(text_data=json.dumps({'drivers':[ driverSerialization(driver) for driver in drivers]}))


        # drivers=None
        # if book:
        #     if location:
        #         tries=1
        #         while(tries<=RiderConsumer.MAX_BOOK_TRIES):
        #             drivers=DriverContoller.getCars(location)
        #             if drivers:
        #                 self.send({"book" :{"drivers":drivers,"status":'OK'}})
        #                 break
        #             time.sleep(1000)
        #             tries+=1
        #         if tries>=RiderConsumer.MAX_BOOK_TRIES:
        #             self.send({"book" :{"drivers":"","status":'NA'}})
        #     else:
        #         self.send(text_data={"book" :{"drivers":"","status":'Invalid location'}})


        # if location and search:
        #     drivers,self.proximityValue=DriverContoller.getCars(location,self.proximityValue)
        #     if drivers:
        #         self.send(text_data={"search" :{"drivers":drivers,"status":'OK'}})
        #     else:# if no drivers:
        #         self.send(text_data={"search" :{"drivers":drivers,"status":'NA'}})
        # self.send(text_data={"search" :{"drivers":drivers,"status":'Invalid location'}})
        # #so after every x interval we send them drivers within a proximity
        # #what if we can't find the drivers (try till x sec then return null drivers)
        # #what if we are searching and we get pinged a locati        
    
def driverSerialization(driver):
    return {
            'username':driver.username,
            'email':driver.email,
            'carId':driver.carId,
            'carNumber':driver.carNumber,
            'carModel':driver.carModel,
            'distance':str(driver.distance),
            'longitude':str(driver.location[0]),
            'latitude':str(driver.location[1]),
        }
        
