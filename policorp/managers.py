from django.db import models

class AvailabilityManager(models.Manager):

    def create_availability(self, when, where, what):
        aval = self.create(when=when, where=where, what=what)
        return aval

    def get_all(self):
        return super().get_queryset().filter(booked=False).order_by("when")

    def get_all_by_task(self, task_name):
        return self.get_all().filter(what__name=task_name).filter(booked=False).order_by("when")

class LocationManager(models.Manager):

    def create_location(self, name):
        loc = self.create(name=name)
        return loc

    def get_all(self):
        return super().get_queryset().all()

class TaskManager(models.Manager):

    def create_task(self, name, duration):
        t = self.create(name=name, duration=duration)
        return t

    def get_all(self):
        return super().get_queryset().all()

class BookingManager(models.Manager):

    def book(self, availability, user):
        b = self.create(availability=availability, user=user)
        availability.book()
        return b

    def get_by_user(self, userObj):
        return super().get_queryset().filter(cancelled=False).filter(user__id=userObj.id).order_by("availability__when")
