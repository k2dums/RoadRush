from django.contrib import admin

# Register your models here.
from .models import RiderClientChannel,DriverClientChannel
from django.contrib import admin

@admin.register(RiderClientChannel)
class RiderClientChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_name','rider')


@admin.register(DriverClientChannel)
class DriverClientChannelAdmin(admin.ModelAdmin):
        list_display = ('channel_name','driver')
