from django.db import models
from .managers import AvailabilityManager, LocationManager, TaskManager

# Create your models here.
class Availability(models.Model):
    when = models.DateTimeField()
    where = models.ForeignKey('Location', on_delete=models.CASCADE, related_name="availableLocations")
    what = models.ForeignKey('Task', on_delete=models.CASCADE, related_name="availableTasks")
    # Managers
    objects = AvailabilityManager()

class Location(models.Model):
    name = models.CharField(max_length=255)

    # Managers
    objects = LocationManager()

class Task(models.Model):
    name = models.CharField(max_length=255)

    # Managers
    objects = TaskManager()
