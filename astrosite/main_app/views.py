from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

def index(request):
    context = None
    return render(request, "main_app/index.html", context)
