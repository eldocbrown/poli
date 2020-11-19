from django.db import models
from .managers import AvailabilityManager, LocationManager, TaskManager

# Create your models here.
class Availability(models.Model):
    when = models.DateTimeField()
    where = models.ForeignKey('Location', on_delete=models.CASCADE, related_name="availableLocations")
    what = models.ForeignKey('Task', on_delete=models.CASCADE, related_name="availableTasks")
    # Managers
    objects = AvailabilityManager()

    def json(self):
        return {
                'id': self.id,
                'when': self.when.isoformat(),
                'where': self.where.json(),
                'what': self.what.json()
        }

class Location(models.Model):
    name = models.CharField(max_length=255)

    # Managers
    objects = LocationManager()

    # Serializer
    def json(self):
        return {
                'id': self.id,
                'name': self.name
        }

class Task(models.Model):
    name = models.CharField(max_length=255)

    # Managers
    objects = TaskManager()

    # Serializer
    def json(self):
        return {
                'id': self.id,
                'name': self.name
        }
