from django.db import models
from .managers import AvailabilityManager, LocationManager, TaskManager, BookingManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Availability(models.Model):
    when = models.DateTimeField()
    where = models.ForeignKey('Location', on_delete=models.CASCADE, related_name="availableLocations")
    what = models.ForeignKey('Task', on_delete=models.CASCADE, related_name="availableTasks")
    booked = models.BooleanField(default=False)

    # Managers
    objects = AvailabilityManager()

    def json(self):
        return {
                'id': self.id,
                'when': self.when.isoformat(),
                'where': self.where.json(),
                'what': self.what.json()
        }

    def book(self):
        self.booked = True
        return self

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

class Booking(models.Model):
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Managers
    objects = BookingManager()
