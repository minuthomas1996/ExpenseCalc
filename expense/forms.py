from . models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2','is_active']


class Detailsform(forms.ModelForm):
    class Meta:
        model=Expense
        fields=[
            'description','category','amount'
        ]
        widgets = {

            'description': forms.TextInput(attrs={'placeholder': 'Description','class': 'form-control',}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'placeholder': 'Amount', 'class': 'form-control'}),
        }

class Filterform(forms.ModelForm):
    class Meta:
        model=Expense
        fields=[
            'category'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }