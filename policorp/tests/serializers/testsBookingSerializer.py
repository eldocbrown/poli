from datetime import datetime, timezone, time, timedelta
from django.test import TestCase
import json
from policorp.models import User, Location, Booking, Task, Availability
from policorp.tests import aux
from policorp.serializers import BookingSerializer, AvailabilitySerializer, UserSerializer

class TestBookingSerializer(TestCase):

    fixtures = ['testsdata.json']

    def test_bookingSerializer_serialize(self):

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
        self.assertEqual(data['user'], UserSerializer(instance = user).data)

    def test_bookingSerializer_deserialize_is_valid(self):

        u1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')

        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        cancelled = False
        note = 'A note for my schedule'
        booking = {
            'availability': {
                'when': now.isoformat(),
                'where': locationid,
                'what': taskid
            },
            'cancelled': cancelled,
            'note': note,
            'user': u1.username
        }

        serializer = BookingSerializer(data=booking)
        self.assertTrue(serializer.is_valid())

    def test_bookingSerializer_deserialize_with_blank_note_is_valid(self):

        u1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')

        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        cancelled = False
        note = ''
        booking = {
            'availability': {
                'when': now.isoformat(),
                'where': locationid,
                'what': taskid
            },
            'cancelled': cancelled,
            'note': note,
            'user': u1.username
        }

        serializer = BookingSerializer(data=booking)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_bookingSerializer_deserialize_without_cancelled_field_is_valid_and_defaults_to_false(self):

        u1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')

        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        cancelled = False
        note = ''
        booking = {
            'availability': {
                'when': now.isoformat(),
                'where': locationid,
                'what': taskid
            },
            'note': note,
            'user': u1.username
        }

        serializer = BookingSerializer(data=booking)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        bookingObj = serializer.save()
        self.assertEqual(bookingObj.cancelled, cancelled)

    def test_bookingSerializer_deserialize_includes_all_fields(self):

        u1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')

        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        cancelled = False
        note = 'A note for my schedule'
        booking = {
            'availability': {
                'when': now.isoformat(),
                'where': locationid,
                'what': taskid
            },
            'user': u1.username,
            'cancelled': cancelled,
            'note': note
        }

        serializer = BookingSerializer(data=booking)

        if (serializer.is_valid(raise_exception=True)):
            self.assertEqual(serializer.data.get('cancelled'), cancelled)
            self.assertEqual(serializer.data.get('note'), note)
            self.assertEqual(serializer.data.get('user').get('username'), u1.username)
            self.assertEqual(serializer.data.get('availability').get('when'), now.isoformat())
            self.assertEqual(serializer.data.get('availability').get('what').get('id'), taskid)
            self.assertEqual(serializer.data.get('availability').get('where').get('id'), locationid)

    def test_bookingSerializer_save_booking_after_deserialize(self):

        u1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')

        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        cancelled = False
        note = 'A note for my schedule'
        booking = {
            'availability': {
                'when': now.isoformat(),
                'where': locationid,
                'what': taskid
            },
            'user': u1.username,
            'cancelled': cancelled,
            'note': note
        }

        serializer = BookingSerializer(data=booking)

        if (serializer.is_valid(raise_exception=True)):
            bookingObj = serializer.save()
            self.assertEqual(bookingObj, Booking.objects.get(pk=bookingObj.id))
            self.assertEqual(bookingObj.availability.when, now)
            self.assertEqual(bookingObj.availability.what.id, taskid)
            self.assertEqual(bookingObj.availability.where.id, locationid)
            self.assertEqual(bookingObj.user, u1)
            self.assertEqual(bookingObj.cancelled, cancelled)
            self.assertEqual(bookingObj.note, note)
