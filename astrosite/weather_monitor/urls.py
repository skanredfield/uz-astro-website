from django.urls import path

from . import views

app_name = "weather_monitor"
urlpatterns = [
    path("", views.index, name="index"),
]