from django.urls import path

from . import views

app_name = "tele_viewer"
urlpatterns = [
    path("", views.index, name="index"),
]