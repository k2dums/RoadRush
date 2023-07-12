from django.contrib import admin
from .models import Trips
# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin
@admin.register(Trips)
class TripsAdmin(OSMGeoAdmin):
    list_display = ("id","rider",'driver','status','origin','destination')
