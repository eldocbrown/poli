from django.urls import path

from . import views

app_name = "policon"

urlpatterns = [
    path("", views.index, name="index"),
]
