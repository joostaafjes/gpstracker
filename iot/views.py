from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Message
import json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def receive(request):
    received_json_data = json.loads(request.body)
    print(f"received json:{received_json_data}")
    message = Message(method=request.method, body=request.body)
    message.save()
    return HttpResponse("Hello, world. You're at the iot index.")
