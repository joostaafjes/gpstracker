from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .gps_tracker import GpsTracker
from .models import Message
import json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def receive(request):
    received_json_data = json.loads(request.body)
    print(f"received json:{received_json_data}")
    message = Message(method=request.method, body=request.body.decode('utf-8'))
    message.save()
    return HttpResponse("Hello, world. You're at the iot index.")


def parse(request):
    for message in Message.objects.filter(parsed=False):
        json_data = json.loads(message.body)
        print(f"json_data:{json_data}")
        data = json_data[0]
        for index in range(1, len(json_data)):
            key = json_data[index]['n']
            value = None
            if 'v' in json_data[index]:
                value = json_data[index]['v']
            elif 'vs' in json_data[index]:
                value = json_data[index]['vs']
            data[key] = value
        print(data)
        if GpsTracker.create(data, message):
            message.parsed = True
            message.save()
    return HttpResponse("parse done")
