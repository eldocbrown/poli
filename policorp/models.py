from django.db import models
from .managers import AvailabilityManager

# Create your models here.
class Availability(models.Model):
    when = models.DateTimeField()

    # Managers
    objects = AvailabilityManager()
