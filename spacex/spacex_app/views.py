from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("You're at the home page!")

def launch(request):
    return HttpResponse("You're at the launch page!")

def crew(request):
    return HttpResponse("You're at the crew page!")

def payload(request):
    return HttpResponse("You're at the payload page!")