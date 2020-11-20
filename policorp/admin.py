from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Location)
admin.site.register(Task)
admin.site.register(Availability)
admin.site.register(User)
admin.site.register(Booking)
