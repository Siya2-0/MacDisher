import json
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth import login, logout,authenticate
from django.db import connection
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import View

from macdisher.views import macdisher_filter
from django.views.decorators.csrf  import csrf_exempt 
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from .forms import LoginForm

from django.utils.decorators import method_decorator
from django.conf import settings


@method_decorator(csrf_exempt , name='dispatch')
class login_user(View):

    def get(self, request):
        loginform=LoginForm()
        return render(request, '_login.html', {"form": loginform})

    def post(self, request):
        
        loginform=LoginForm(request.POST)
        #user1=LoginForm(request.POST)
        if True:
               
            uname=request.POST.get('username')
            pword=request.POST.get('password')
            next=request.POST.get('next')
            if uname is None and pword is None:
                list=request.body.decode('utf-8')
                DataList=list.split("&")
        
                for data in DataList:
                    if(data.startswith("username=")):
                        uname=data[data.find("=")+1:]
                    if(data.startswith("password=")):
                        pword=data[data.find("=")+1:]

            

          
            user=authenticate(username=uname, password=pword)
     
            if(user is not None):
                settings.username=uname
                if  next  is not None  and next != "":
                    login(request, user)
                    return  redirect(request.POST.get('next'))
                else:
                    login(request, user)
                    return  redirect(('/mcdisher/home/'))
                
            else:
                settings.username=""
                return render(request, "_login.html", {"form":loginform, "log": "","logg": "pword"}, status=202)
            


            
def logout_user(request):
    logout(request)
    settings.username=""
    return redirect("/mcdisher/home/")

