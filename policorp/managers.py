from django.db import models

class AvailabilityManager(models.Manager):

    def create_availability(self, when, where):
        aval = self.create(when=when, where=where)
        return aval

    def get_all(self):
        return super().get_queryset().all().order_by("when")

class LocationManager(models.Manager):

    def create_location(self, name):
        loc = self.create(name=name)
        return loc

    def get_all(self):
        return super().get_queryset().all()
