from django import forms
from django.forms import ModelForm
from . import models

class TaskForm(forms.ModelForm):
    # add calender and time widgets
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))

    class Meta:
        model = models.Task # our model
        fields = '__all__' # use all fields