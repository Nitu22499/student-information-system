from django import forms
from django.contrib.auth.forms import UserCreationForm
from Attendence.models import Attendence

class AttendenceForm(forms.ModelForm):
    class Meta:
        model = Attendence
        fields = ('__all__')
