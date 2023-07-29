from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='driverIndex'),
    path('test/',views.driver_test,name='driverTest'),
    path('login/',views.loginView,name='driver_login'),
    path('logout/',views.logoutView,name='driver_logout'),
    path('<int:carId>/',views.driver_details,name='driverDetails'),
    path('register/',views.registerView,name='driver_register'),
    path('update/availability/<int:carId>',views.updateOccupiedStatus,name='driveUpdateAvailability'),
    path('update/location/<int:carId>',views.updateDriverLocation,name='driverUpdateLocation')
    #endTrip
]