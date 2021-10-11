from django.db import models


class Message(models.Model):
    method = models.CharField(max_length=10)
    body = models.CharField(max_length=1000)
    parsed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class GpsTrackerMessage(models.Model):
    deveui = models.CharField(max_length=100)
    date = models.DateTimeField()
    payload = models.CharField(max_length=1000)
    latitude = models.DecimalField(max_digits=12, decimal_places=6)
    longitude = models.DecimalField(max_digits=12, decimal_places=6)
    alarm = models.BooleanField(default=False)
    battery = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    battery_perc = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    led_activity = models.BooleanField(default=False)
    movement_detection = models.IntegerField()
    roll = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    pitch = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    altitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    hdop = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    message = models.OneToOneField(Message, on_delete=models.SET_NULL, null=True)


class LoraMessage(models.Model):
    deveui = models.CharField(max_length=100)
    date = models.DateTimeField()
    locOrigin = models.CharField(max_length=1000)
    latitude = models.DecimalField(max_digits=12, decimal_places=6)
    longitude = models.DecimalField(max_digits=12, decimal_places=6)
    radius = models.DecimalField(max_digits=12, decimal_places=6)
    locAccuracy = models.DecimalField(max_digits=12, decimal_places=6)
    locPrecision = models.DecimalField(max_digits=12, decimal_places=6)
    locTime = models.DateTimeField()
    message = models.OneToOneField(Message, on_delete=models.SET_NULL, null=True)
