from django.conf import settings
from django.db import models




class DockMac(models.Model):
    id = models.IntegerField(primary_key=True)
    allocation = models.CharField(max_length=255, blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    mac = models.CharField(max_length=255, blank=True, null=True)
    metastring = models.CharField(max_length=255, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dock_mac'

class Mac(models.Model):
    allocation = models.CharField(max_length=255, blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    mac = models.CharField(unique=True, max_length=255, blank=True, null=True)
    metastring = models.CharField(max_length=255, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mac'



    

class Device(models.Model):
    DeviceName=models.CharField(max_length=30)

    def __str__(self):
        return self.DeviceName
    

class Allocation(models.Model):
    AllocationType=models.CharField(max_length=30)

    def __str__(self):
        return self.AllocationType

