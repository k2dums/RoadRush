from django.shortcuts import render,redirect
from controllers.controllers import RiderController
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.urls import reverse
from rest_framework import generics
from .models import Rider
from django.contrib.auth import authenticate, login, logout
from authentication.models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Error':"User not logged in"},status=404)
    user=None
    try:
        user=Rider.objects.get(username=request.user.username)
    except:
        return JsonResponse({'Error':'Current User is not a rider'})
    if user:
        response=user.serialize()
        if user.currentTrip:
            driver=user.currentTrip.driver
            carId=driver.carId
            response['carId']=carId
        return JsonResponse(response)

 
@csrf_exempt
def loginView(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        rider=authenticate(request,email=email,password=password)
        if rider:
            rider=Rider.objects.get(email=email)
            login(request,rider)
            return JsonResponse(rider.serialize(),status=200)
        else:
            return JsonResponse({'error':'invalid email or password'})

    return render(request,'rider/login.html')

def logOutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('riderTest'))

@csrf_exempt
def registerView(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        username=request.POST.get('username')

        rider=RiderController.registerRider(username,email,password)
        if isinstance(rider,Rider):
            login(request,rider)
            return JsonResponse(rider.serialize(),status=200)
        else:
            return JsonResponse(rider,status=404,)


    return render(request,'rider/register.html')

@login_required
def rider_details(request,username):
    if (request.user.username==username):
        details=RiderController.getRiderDetails(username)
        return JsonResponse({'rider':details},safe=False)
    return JsonResponse({'error':'Bad Request'},status=400)
    
@login_required
def book(request,username):
    return HttpResponse(request.user.username+' has requested to book')
    # carId=-1
    # location=(-1,-1)
    # destination=(-1,-1)
    # RiderController.book(carId,location,destination)


def rider_test_loc(request):
    return render(request,'rider/test_loc.html',{'username':request.user.username})

def rider_test(request):
    rider=RiderController.getRider(request.user.username)
    trip=rider.currentTrip
    if rider.currentTrip:
        trip=rider.currentTrip.serialize()
    return render(request,'rider/index.html',{'useremail':request.user,'username':rider.username,'currentTrip':trip})

def all_riders(request):
    riders=list(Rider.objects.values())
    # rider_list=serializers.serialize('json',list(riders),fields=['username','email'])
    return JsonResponse(riders,safe=False,json_dumps_params={'indent': 2})