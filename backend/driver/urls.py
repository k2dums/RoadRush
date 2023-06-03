from django.urls import path
from . import views


urlpatterns = [
    path('test/',views.index,name='driverTest'),
    path('login/',views.loginView,name='driver_login'),
    path('<int:carId>/',views.driver_details,name='driverDetails'),
    path('register/',views.registerView,name='driver_register'),
    path('update/availability/<int:carId>',views.updateOccupiedStatus,name='driveUpdateAvailability'),
    path('update/location/<int:carId>',views.updateDriverLocation,name='driverUpdateLocation')
    #endTrip
]