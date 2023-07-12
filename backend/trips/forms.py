from .models import Trips
from django import forms

class TripForm(forms.ModelForm):
    class Meta:
        model=Trips
        fields='__all__'
