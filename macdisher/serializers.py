from abc import ABC
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Mac
from django.utils.dateparse import parse_datetime

# Django Rest Framework serializers go here
class MacSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mac
        fields="__all__"

