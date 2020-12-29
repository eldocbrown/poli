from django.contrib import admin
from .models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "duration")

class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "is_supervisor")

# Register your models here.

admin.site.register(Location, LocationAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Availability)
admin.site.register(User, UserAdmin)
admin.site.register(Booking)
