from datetime import datetime, timezone, time, timedelta
from django.test import TestCase
import json
from policorp.models import User, Location, Booking, Task, Availability
from policorp.tests import aux
from policorp.serializers import BookingSerializer, AvailabilitySerializer
import sys

class TestBookingSerializer(TestCase):

    def test_bookingSerializer_full(self):

        # User
        username = "foo"
        email = "foo@example.com"
        password = "example"
        user = aux.createUser("foo", "foo@example.com", "example")

        # Availability
        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)

        # Booking
        b = Booking.objects.book(a1, user)
        serializer = BookingSerializer(instance=b)
        data = serializer.data

        self.assertEqual(set(data.keys()), set(['id', 'availability', 'user', 'cancelled', 'note']))
        self.assertEqual(data['cancelled'], False)
        self.assertEqual(data['note'], '')
        self.assertEqual(data['availability'], AvailabilitySerializer(instance = a1).data)
        self.assertEqual(data['user'], user.username)
