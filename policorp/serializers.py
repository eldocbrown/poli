from rest_framework import serializers
from policorp.models import Availability, User, Booking #, Location, Task,

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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    availability = AvailabilitySerializer()

    class Meta:
        model = Booking
        fields = ['id', 'availability', 'user', 'cancelled', 'note']
        depth = 1
