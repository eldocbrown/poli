from django.db import models

class AvailabilityManager(models.Manager):

    def create_availability(self, when):
        aval = self.create(when=when)
        return aval

    def get_all(self):
        return super().get_queryset().all().order_by("when")
