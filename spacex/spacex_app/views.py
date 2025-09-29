from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .helper_functions import api_request
import operator

def home(request):
    return HttpResponse("You're at the home page!")

def launch(request):
    api_url = "https://api.spacexdata.com/v4/launches"
    data = api_request(api_url)
    data.reverse()
    return JsonResponse(data, safe=False)

def crew(request):
    api_url = "https://api.spacexdata.com/v4/crew"
    data = api_request(api_url)
    data.sort(key=operator.itemgetter("name"))
    return JsonResponse(data, safe=False)

def payload(request):
    api_url = "https://api.spacexdata.com/v4/payloads"
    data = api_request(api_url)
    data.sort(key=operator.itemgetter("name"))
    return JsonResponse(data, safe=False)