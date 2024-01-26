from django.urls import path, include
from . import views
from django.views.decorators.csrf  import csrf_exempt
app_name="macd"

urlpatterns = [
    # Base production URLs
    path("", views.macdisher_index, name='macdisher_home'),
    path("home/", views.macdisher_index, name='macdisher_home'),

    path("search/", views.macdisher_filter, name='fitler'),
    path("search/<str:list>", views.macdisher_export_CSV, name='export_to_csv'),

    path("search/<int:pagenumber>/<str:list>", views.macdisher_paginate, name='paginate'),
    path("search/<str:list>", views.macdisher_export_CSV, name='export_to_csv'),
    path("search/<int:pagenumber>/", views.Pending_Pagination, name='paginate_pending'),

    path("assign/", views.macdisher_assign, name="assignmac"),


    path("reserve/", views.macdisher_reserve, name='reserver'),
    path("reserve/<int:pagenumber>/<int:count>", views.macdisher_pagniate_GET_MAC, name='paginate_GET_MAC'),

    #API

    path("getMAC/", csrf_exempt(views.Post_Reserve_Request), name='API_reserver'),
    path("getMAC", csrf_exempt(views.Post_Reserve_Request), name='API_reserver'),
    path("allMAC/", views.POST_AllMac, name='API_allmac'),
    path("allMAC", views.POST_AllMac, name='API_allmac'),
    path("assignMAC/", views.POST_AssignMac, name="API_Assign"),
    path("assignMAC", views.POST_AssignMac, name="API_Assign"),

    #delete
     #NEED TO REGEX AND REWRITE THESE URL PATTERN
]
