from abc import ABC, abstractmethod
import json
from django.shortcuts import render

# from ..config.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action
# Create your views here.
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from config.permissions import ApiPermission
from .repo import DeviceRepo, DeviceTypeRepo

class BaseApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    permission_slug = "key.create"

    def __init__(self, family_code):
       self.family_code = family_code
       self.device_repo = DeviceRepo(family_code=family_code)
       self.device_type_repo = DeviceTypeRepo(family_code=family_code)

    @abstractmethod
    def create_get_serializer(self, devices, *args, **kwargs):
       """
       Serializer with most relevant fields for the API model
       """

    @abstractmethod
    def create_initial_serializer(self, request_data):
       """
       The initianl serializer contains the minimal fields to verify
       and determine the correct serializer later on
       """

    @abstractmethod
    def create_primary_serializer(self, device_code, request_data):
       """
       This serializer should be the once that is used based on the
       device code provided

       It should check for all the required meta test fields
       """

    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        devices = self.device_repo.list(request)
        serializer = self.create_get_serializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Post a message on the specified conversation
    def post(self, request, *args, **kwargs):
        pass

