import json
from channels.generic.websocket import WebsocketConsumer
from enum import Enum
from controllers.controllers import DriverContoller,TripsController
import time
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
        if not self.rider_status:
            self.rider_status=RiderStatus.NONE
        print('Connection request from RIDER:%s' % self.rider_name)
        self.accept()
        

    def disconnect(self,close_code):
        print('[RIDER] Disconnected RIDER:%s' % self.rider_name)
    
  
    def receive(self, text_data):
        #limit the rate at which we are getting receive per 1 sec receive only 1 location ping 
        try:
            text_data_json=json.loads(text_data)
        except:
            self.send(json.dumps({"Error":'Data not in json format',"status":300}))
            return 
        location=text_data_json.get('location')#will get location per 5sec interval
        destination=text_data_json.get('destination')

        test=text_data_json.get('test')
        search=text_data_json.get('search') #analogus to booking
        endTrip=text_data_json.get('endTrip')
        bid=text_data_json.get('bid')

        print(f'Data sent by {self.rider_name}-{text_data}')

        if (test):
            emergency=text_data_json.get('emergency')
            self.carType=text_data_json.get('carType')
            location=text_data_json.get('location')
            self.send(text_data=json.dumps({'Success':'Test query received successfully'}))
            self.send(text_data=json.dumps({"Sent by user":text_data_json}))

            if not location:
                self.send(text_data=json.dumps({'error':'No location sent'}))
            if search:
                trip=DriverContoller.getCarsforBooking(self.rider_name,location,destination,self.carType,self.priority)
                print('Trip made by server',trip)
                self.send(text_data=json.dumps(trip.serialize()))
            else:
                drivers=DriverContoller.getCars(location,self.carType)
                self.send(text_data=json.dumps({'drivers':[ driverSerialization(driver) for driver in drivers]}))
            return 

        if  search: #if rider wants to search
            emergency=text_data_json.get('emergency')
            self.carType=text_data_json.get('carType')

            if emergency:
                self.priority=DriverContoller.Priority.EMERGENCY
            
            self.priority=DriverContoller.Priority.NORMAL
            if location and location.get('longitude') and  location.get('latitude'):
                if destination and destination.get('longitude') and destination.get('latitude'):
                    # tries=1
                    # while(tries<=RiderConsumer.MAX_BOOK_TRIES):
                    response,flag=DriverContoller.getCarsforBooking(self.rider_name,location,destination,self.carType)
                    if flag:
                        #if flag is true the response is a Trip instance
                        print(f"[SERVER] Data sent to the [user:{self.rider_name}],{response}")
                        self.send(text_data=json.dumps({"trip":response.serialize(),"status":200}))
                    else:
                        #if flag is flase it returns a repsonse
                        print(f"[SERVER] Data sent to the [user:{self.rider_name}],{response}")
                        self.send(text_data=json.dumps(response))
                        # break
                        # time.sleep(4000)
                        # tries+=1
                        # if tries>=RiderConsumer.MAX_BOOK_TRIES:
                        #     self.send(text_data=json.dumps({"book" :{"trip":None,"status":'NA'}}))
                else:#Invalid/Missing origin location
                    response={"Error":"Invalid Destination location",'status':400}
                    if not destination:
                        response={"Error":"Destination location not given",'status':400}
                    self.send(text_data=json.dumps(response))
            else:#Invalid/Missing destination location
                response={"Error":'Invalid Origin location','status':400}
                if not location:
                    response={'Error':'Origin Location not given','status':400}
                print(f"[SERVER] Data sent to the [user]:{self.rider_name}],{response}")
                self.send(text_data=json.dumps(response))
        elif  bid:
            pass
        elif endTrip:
            carId=text_data_json.get('carId')
            action=text_data_json.get('action')
            if not carId:
                self.send(json.dumps({"Error":"carId not given"}))
                return 
            if not action:
                self.send(json.dumps({"Error":"action not given"}))
                return
            response=TripsController.endTrip(carId,self.rider_name,action)
            print(f"[SERVER] Data sent to [{self.rider_name}]",response)
            self.send(json.dumps(f"{response}"))
        else:
            self.send("No valid action was sent (search,bid,endTrip)")
            
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
        


   