from django.shortcuts import render,redirect
from rider.controller import RiderController
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.urls import reverse
from rest_framework import generics
from .models import Rider
from django.contrib.auth import authenticate, login, logout
from authentication.models import User
# Create your views here.


def test(request):
    return render(request,'rider/index.html')


def loginView(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        rider=authenticate(request,email=email,password=password)
        if rider:
            rider=Rider.objects.get(email=email)
            return JsonResponse(rider.serialize(),status=200)
        else:
            return JsonResponse({'error':'invalid email or password'})

    return render(request,'rider/login.html')

def registerView(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        username=request.POST.get('username')

        rider=RiderController.registerRider(username,email,password)
        if isinstance(rider,Rider):
            return JsonResponse(rider.serialize(),status=200)
        else:
            return JsonResponse(rider,status=404)


    return render(request,'rider/register.html')


def rider_details(request,username):
    details=RiderController.getRiderDetails(username)
    return JsonResponse({'rider':details},safe=False)
def book(request):
    carId=-1
    location=(-1,-1)
    destination=(-1,-1)
    RiderController.book(carId,location,destination)


def rider_test_loc(request,username):
    return render(request,'rider/test_loc.html',{'username':username})