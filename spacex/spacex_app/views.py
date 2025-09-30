from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .helper_functions import api_request
import operator

def home(request):
    return render(request, "home.html")

def launch(request):
    api_url = "https://api.spacexdata.com/v4/launches"
    launches = api_request(api_url)
    launches.reverse()
    return render(request, "launch.html", {"launches": launches})

def crew(request):
    api_url = "https://api.spacexdata.com/v4/crew"
    crew_members = api_request(api_url)
    crew_members.sort(key=operator.itemgetter("name"))
    return render(request, "crew.html", {"crew_members": crew_members})

def payload(request):
    api_url = "https://api.spacexdata.com/v4/payloads"
    payloads = api_request(api_url)
    payloads.sort(key=operator.itemgetter("name"))
    return render(request, "payload.html", {"payloads": payloads})