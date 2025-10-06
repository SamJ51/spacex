from django.shortcuts import render
from .models import CrewMember, Payload, Launch

def home(request):
    return render(request, "home.html")

def launch(request):
    launches = Launch.objects.all().order_by('-date_utc')
    return render(request, "launch.html", {"launches": launches})

def payload(request):
    payloads = Payload.objects.all().order_by('name')
    return render(request, "payload.html", {"payloads": payloads})

def crew(request):
    crew = CrewMember.objects.all().order_by('name')
    return render(request, "crew.html", {'crew': crew})