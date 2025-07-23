from django.forms import ModelForm
from .models import Task
from django.db import models
from django import forms
from django.utils import timezone


class TaskForm(ModelForm):
    due_date = forms.DateField(
        widget = forms.DateInput(
            attrs = {
                'class': 'form-control',
                'type': 'date'
            }
        ),
        initial=timezone.now()
    )
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'priority']