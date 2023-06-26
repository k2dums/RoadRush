from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns=[
    path('',views.test,name='riderTest'),
  

    #-------------------API route------------------------#
    path('login/',views.loginView,name='rider_login'),
    path('logout/',views.logOutView,name='rider_logout'),
    path('register/',views.registerView,name='rider_register'),
    path('<str:username>/',views.rider_details,name='rider_details'),
    path('book/<str:username>/',views.book,name='rider_book'),
    path('<str:username>/test_loc/',views.rider_test_loc,name='rider_test_loc'),
    path('all_riders',views.all_riders)
]