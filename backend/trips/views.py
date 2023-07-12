from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Trips
from django.http import JsonResponse
from .forms import TripForm
# Create your views here.

class TripDetailView(DetailView):
    model=Trips
    pk_url_kwarg = 'id'
    def get(self,request,*args,**kwargs):
        trip=self.get_object()#gets object based on the pk/id
        if trip:
            return JsonResponse(trip.serialize(),status=200,json_dumps_params={'indent': 2})
        else:
            return JsonResponse({"Error":"No such trip"},status=400,)