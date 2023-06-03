from django.contrib.gis.admin import OSMGeoAdmin
from .models import Driver
from django.contrib import admin
@admin.register(Driver)
class DriverAdmin(OSMGeoAdmin):
    list_display = ('username', 'location','carId')
