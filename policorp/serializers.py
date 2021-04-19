from rest_framework import serializers
from policorp.models import Availability #, Location, Task, User, Booking

# class LocationSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Location
#         fields = ['id', 'name']
#
# class TaskSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Task
#         fields = ['id', 'name', 'duration']

class AvailabilitySerializer(serializers.ModelSerializer):

    #where = LocationSerializer(many=False, read_only=True)
    #what = TaskSerializer(many=False, read_only=True)

    class Meta:
        model = Availability
        fields = ['id', 'when', 'where', 'what', 'booked']
        depth = 1
