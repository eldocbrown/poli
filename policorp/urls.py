from django.urls import path

from . import views

app_name = "policorp"

urlpatterns = [
    path("tasks/", views.tasks, name="tasks"),
    path("availabilities/<int:taskid>", views.availabilities, name="availabilities"),
    path("book/<int:availabilityid>", views.book, name="book"),
]
