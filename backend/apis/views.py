from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def api_path(request):
    driverPath={
    'driver':{
           'driver/test/':{
                    'method':'GET',
                    'description':'For testing server',
                    },
   'driver/login/':{
                    'method':'POST',
                    'description':'for driver login'
   },
   'driver/<int:carId>/':{
                    'method':'GET',
                    'description':'Returns the driver details'
   },
   'driver/register/':{
                    'method':'POST',
                    'description':'for registering the driver'
   },
   'driver/update/availability/<int:carId>':{
                    'method':'GET',
                    'description':'for checking the availabilty of the driver based on cardId'
   },
   'driver/update/location/<int:carId>':{
                    'method':'POST',
                    'description':'for updating the driver location based on carId'
   }
    },

'rider':{
    'rider/login':{
                    'method':'POST',
                    'description':'for getting rider login'
    },
    'rider/register':{
                    'method':'POST',
                    'description':'for rider registration'
    },
    'rider/<str:username>/':{
                    'method':'GET',
                    'description':'for rider details based on username'
    },
    'rider/book/<str:username>/':{
                    'method':'POST',
                    'description':'for booking the rider car'
    },
    'rider/<str:username>/test_loc/':{
                'method':'GET',
                    'description':'Testing purpose getting the rider location baed on username'
    },

}
    
 
    }

    return JsonResponse({'UrlPaths':driverPath},json_dumps_params={'indent': 2})
 