from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.forms import CharField
from django.db import models



class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password',)
        widgets={
            'username':forms.TextInput(attrs={'class': "form-control form-control-lg  border border-white",'placeholder':"Username"}),
            'password':forms.PasswordInput(attrs={'class': 'form-control form-control-lg','placeholder':"password"}),
        }
        required={
            'username',
            'password',
        }
        help_texts={
            "username":None,
            'password': None,
        }
        labels={
            'name': None,
            'password': None,
        }

    

    
