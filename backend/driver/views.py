from django.shortcuts import render,redirect
from controllers.controllers import DriverContoller
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Driver
from authentication.models import User
from django.contrib.gis.geos import Point
from django.contrib.auth import authenticate, login, logout
import json
# Create your views here.
def index(request):
    return render(request,'driver/index.html')
def loginView(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:

            driver=authenticate(request,email=email,password=password)
            if driver:
                login(request,driver)
                driver=Driver.objects.get(email=email)
                driver_details={
                    'username':driver.username,
                    'email':driver.email,
                    'carModel':driver.carModel,
                    'carId':driver.carId,
                    'carNumber':driver.carNumber,
                }
                return JsonResponse({'driver':driver_details},status=200)
            else:
                return JsonResponse({'error':'invalid email or password'})
        except  Exception as e:
            print(e)
            return HttpResponse(e)
     
       

    return render(request,'driver/login.html')

def registerView(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        username=request.POST.get('username')
        carModel=request.POST.get('carModel')
        carNumber=request.POST.get('carNumber')
        carId=request.POST.get('carId')

        driver=DriverContoller.registerDriver(username=username,email=email,password=password,carModel=carModel,carNumber=carNumber,carId=carId)
        if isinstance(driver,Driver):
            login(request,driver)
            return JsonResponse(driver.serialize(),status=200)
        else:
            return JsonResponse(driver,status=404)
       
    return render(request,'driver/register.html')


def driver_details(request,carId):
    details=DriverContoller.driverDetails(carId)
    return JsonResponse({'driver':details},safe=False)

def updateOccupiedStatus(request,carId):
    occupiedStatus=False
    DriverContoller.updateDriverOccupiedStatus(carId,occupiedStatus)

def endTrip(request,carId):
    if request.method=='POST':
        DriverContoller.endTrip(carId)

def updateDriverLocation(request,carId):
    # {"longitude": 88.563875, "latitude": 27.2948094} 3001
    lat=1
    long=1
    location={long,lat}
    DriverContoller.updateDriverLocation(carId,location)
    details=DriverContoller.driverDetails(carId)
    return JsonResponse({'driver':details},safe=False)
