from django.db import models
from django.contrib.auth.base_user import BaseUserManager

class AvailabilityManager(models.Manager):

    def create_availability(self, when, where, what):
        avail = self.create(when=when, where=where, what=what)
        return avail

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

    def get_by_location_and_date(self, locationObj, date):
        return super().get_queryset().filter(cancelled=False).filter(availability__where=locationObj).filter(availability__when__date=date).order_by("availability__when")

class MyUserManager(BaseUserManager):

    def create_supervisor(self, username, email, password):
        u = self.create(username=username, email=email)
        u.set_password(password)
        u.is_supervisor = True
        u.save()
        return u

    def create_user(self, username, email, password):
        u = self.create(username=username, email=email)
        u.set_password(password)
        u.save()
        return u

    def create_superuser(self, username, email, password):
        u = self.create(username=username, email=email)
        u.set_password(password)
        u.is_superuser = True
        u.save()
        return u
