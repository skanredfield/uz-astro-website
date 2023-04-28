from django.shortcuts import render

def index(request):
    context = None
    return render(request, "tele_viewer/index.html", context)
