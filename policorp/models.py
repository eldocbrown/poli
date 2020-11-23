from django.db import models
from .managers import AvailabilityManager, LocationManager, TaskManager, BookingManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

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

    # Serializer
    def json(self):
        return {
                'id': self.id,
                'when': self.when.isoformat(),
                'where': self.where.json(),
                'what': self.what.json()
        }

    # Operations
    def book(self):
        self.booked = True
        self.save()
        return self

    def free(self):
        self.booked = False
        self.save()
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
    duration = models.PositiveIntegerField()

    # Managers
    objects = TaskManager()

    # Serializer
    def json(self):
        return {
                'id': self.id,
                'name': self.name,
                'duration': self.duration
        }

class Booking(models.Model):
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)

    # Managers
    objects = BookingManager()

    # Serializer
    def json(self):
        return {
                'id': self.id,
                'availability': self.availability.json(),
                'username': self.user.username
        }

    # Operations
    def cancel(self):
        self.availability.free()
        self.cancelled = True
        self.save()
        return self
