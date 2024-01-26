from django.urls import path, include
from . import views

from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie

app_name="loginAPP"
urlpatterns = [
    # Base production URLs
    path("", views.login_user.as_view(), name='loginAuto'),

    path("login/",( views.login_user.as_view()), name='login'),
    path("login",( views.login_user.as_view()), name='login'),
    
    path("logout/", (views.logout_user), name="logout"),
    #NEED TO REGEX AND REWRITE THESE URL PATTERN

]