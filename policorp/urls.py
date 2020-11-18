from django.urls import path

from . import views

app_name = "policorp"

urlpatterns = [
    path("tasks/", views.tasks, name="tasks")
]
