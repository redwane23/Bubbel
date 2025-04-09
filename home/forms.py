
from cProfile import label
import email
from tkinter import Widget
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class JoinForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=CustomUser
        fields =('Username','email')
    
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
