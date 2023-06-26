from django.shortcuts import render,redirect
from rider.controller import RiderController
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.urls import reverse
from rest_framework import generics
from .models import Rider
from django.contrib.auth import authenticate, login, logout
from authentication.models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.


def test(request):
    return render(request,'rider/index.html',{'useremail':request.user,'username':request.user.username})

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
            return JsonResponse(rider,status=404)


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


def rider_test_loc(request,username):
    return render(request,'rider/test_loc.html',{'username':username})


def all_riders(request):
    riders=list(Rider.objects.values())
    # rider_list=serializers.serialize('json',list(riders),fields=['username','email'])
    return JsonResponse(riders,safe=False,json_dumps_params={'indent': 2})