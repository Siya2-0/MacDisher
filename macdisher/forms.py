from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.forms import CharField
from django.db import models

from .models import Device, Allocation

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)
        widgets={
            'username':forms.TextInput(attrs={'className': 'form-control'}),
            'password':forms.TextInput(attrs={'className': 'form-control'}),
        }

class PaginationForm(forms.ModelForm):
    class Meta:
        fields = ('offset', 'limit', )

 


class DropDownFilterForm(forms.Form):
    MacInput=forms.CharField(required=False,label="MAC", max_length=100, widget=forms.TextInput(attrs={'class': "form-control form-control-lg", 'id':"macInput"}))
    DeviceInput=forms.ModelChoiceField(queryset=Device.objects.all(), label="Device", initial=Device.objects.get(pk=28).pk)
    AllocationInput=forms.ModelChoiceField(queryset=Allocation.objects.all(), label="Allocation state", initial=Allocation.objects.get(pk=3).pk)

    DeviceInput.widget.attrs.update({"id":"DeviceField", "class": "form-control form-control-lg"})
    AllocationInput.widget.attrs.update({'id':"AllocationField", "class":"form-control form-control-lg"})


class ReserveMacForm(forms.Form):
    Count=forms.IntegerField(required=True,label="Count")
    Device=forms.ModelChoiceField(required=True,queryset=Device.objects.all().exclude(pk=28), label="Device")
    MetaData=forms.CharField(required=False, label='Meta Data', max_length=100)

    Count.widget.attrs.update({"class": "form-control form-control-lg"})
    Device.widget.attrs.update({"class": "form-control form-control-lg"})
    MetaData.widget.attrs.update({"class": "form-control form-control-lg"})
