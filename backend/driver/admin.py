from django.contrib.gis.admin import OSMGeoAdmin
from .models import Driver
from django.contrib import admin
@admin.register(Driver)
class DriverAdmin(OSMGeoAdmin):
    list_display = ('carId','username', 'location','carId')
