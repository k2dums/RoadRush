from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns=[
    path('test/',views.test,name='riderTest'),
  

    #-------------------API route------------------------#
    path('login/',views.loginView,name='rider_login'),
    path('register/',views.registerView,name='rider_register'),
    path('<str:username>/',views.rider_details,name='rider_details'),
    path('book/<str:username>/',views.book,name='rider_book'),
    path('<str:username>/test_loc/',views.rider_test_loc,name='rider_test_loc'),
]