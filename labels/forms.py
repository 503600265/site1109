from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LabelingForm(forms.ModelForm):

    class Meta:
        model = Labeling
        fields = ('name', 'description','image')
        exclude = ('user',)
