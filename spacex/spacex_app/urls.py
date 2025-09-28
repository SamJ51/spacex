from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("launch", views.launch, name="launch"),
    path("crew", views.crew, name="crew"),
    path("payload", views.payload, name="payload"),
]