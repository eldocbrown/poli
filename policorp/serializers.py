from rest_framework import serializers
from datetime import datetime
from policorp.models import Availability, User, Booking, Location, Task

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'name']

class AvailabilityDateTimeField(serializers.DateTimeField):

    def to_representation(self, value):
        return value.isoformat()

class AvailabilitySerializer(serializers.ModelSerializer):

    when = AvailabilityDateTimeField()

    class Meta:
        model = Availability
        fields = ['id', 'when', 'where', 'what', 'booked']

    def to_representation(self, instance):
        self.fields['what'] = TaskSerializer(read_only=True)
        self.fields['where'] = LocationSerializer(read_only=True)
        return super().to_representation(instance)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    availability = AvailabilitySerializer(read_only=False)
    note = serializers.CharField(allow_blank=True, read_only=False)

    class Meta:
        model = Booking
        fields = ['id', 'availability', 'user', 'cancelled', 'note']

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super().to_representation(instance)

    def create(self, validated_data):

        # Create a new availability
        availabilityData = validated_data.pop('availability')

        location = Location.objects.get(pk=availabilityData.pop('where').id)
        when = availabilityData.pop('when')
        task = Task.objects.get(pk=availabilityData.pop('what').id)
        availabilityObj = Availability.objects.create_availability(when, location, task)

        # Get the user
        userObj = User.objects.get(username=validated_data.pop('user').pop('username'))

        # Create a new booking and book the availability just created
        bookingObj = Booking.objects.book(availabilityObj, userObj, validated_data.get('note'))
        return bookingObj
