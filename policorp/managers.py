from django.db import models

class AvailabilityManager(models.Manager):

    def create_availability(self, when, where, what):
        aval = self.create(when=when, where=where, what=what)
        return aval

    def get_all(self):
        return super().get_queryset().all().order_by("when")

    def get_all_by_task(self, task_name):
        return self.get_all().filter(what__name=task_name)

class LocationManager(models.Manager):

    def create_location(self, name):
        loc = self.create(name=name)
        return loc

    def get_all(self):
        return super().get_queryset().all()

class TaskManager(models.Manager):

    def create_task(self, name):
        t = self.create(name=name)
        return t

    def get_all(self):
        return super().get_queryset().all()
