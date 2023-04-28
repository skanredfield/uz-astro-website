from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import WeatherData
from .graph import *


def index(request):
    data = WeatherData.objects.order_by("-reading_date")[:5]
    context = {"weather_data": data}
    return render(request, "weather_monitor/index.html", context)

