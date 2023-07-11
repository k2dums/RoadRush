from django.urls import path
from . import views
from django.views.generic import TemplateView,RedirectView

urlpatterns=[
    #-------------------API route------------------------#
    path('',views.index,name='index'),
    path('test/',views.rider_test,name='rider_test'),
    path('test_loc/',views.rider_test_loc,name='rider_test_loc'),
    path('login/',views.loginView,name='rider_login'),
    path('logout/',views.logOutView,name='rider_logout'),
    path('register/',views.registerView,name='rider_register'),
    path('<str:username>/',views.rider_details,name='rider_details'),
    path('book/<str:username>/',views.book,name='rider_book'),
    path('all_riders',views.all_riders),
]