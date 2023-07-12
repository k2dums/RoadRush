from django.urls import path
from . import views

urlpatterns=[
    path('<str:id>/',views.TripDetailView.as_view(),name='tripDetails'),
]