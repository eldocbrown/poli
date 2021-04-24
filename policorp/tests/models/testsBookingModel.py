from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from policorp.models import Availability, Booking
from policorp.tests import aux
import json

class TestBooking(TestCase):

    fixtures = ['testsdata.json']

    def test_book_availability_user(self):
        """ Booking an availability registers who boooked it """
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        b = Booking.objects.book(availability, user)
        self.assertEqual(len(Booking.objects.filter(availability=availability)), 1)
        self.assertEqual(Booking.objects.filter(availability=availability)[0].user, user)

    def test_book_availability_is_booked(self):
        """ Booking an availability marks it as booked """
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        b = Booking.objects.book(availability, user)
        availability = Availability.objects.get(pk=1)
        self.assertTrue(availability.booked)

    def test_booking_serialize_json(self):
        """ GIVEN a booking; WHEN requesting json serialization; THEN it should be returned in json format """
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        booking = Booking.objects.book(availability, user)

        expected_json = {'id': 1, 'availability': availability.json(), 'username': user.username }

        self.assertEqual(booking.json()["availability"] , expected_json["availability"])
        self.assertEqual(booking.json()["username"], expected_json["username"])

    def test_booking_get_my_bookings(self):
        """ GIVEN 2 bookings, 1 for user foo and 1 for user juan; WHEN requesting user bookings for foo; THEN 1 booking with user foo should be returned """
        availability1 = Availability.objects.get(pk=1)
        user1 = aux.createUser("foo", "foo@example.com", "example")
        b1 = Booking.objects.book(availability1, user1)
        availability2 = Availability.objects.get(pk=2)
        user2 = aux.createUser("juan", "juan@example.com", "example")
        b2 = Booking.objects.book(availability2, user2)
        bookingsforfoo = Booking.objects.get_by_user(user1)

        self.assertEqual(len(bookingsforfoo), 1)
        self.assertEqual(bookingsforfoo[0].user, user1)

    def test_booking_get_my_bookings_ordered(self):
        """ GIVEN 2 bookings for user foo; WHEN requesting bookings for user foo; THEN 2 bookings should be returned ordered by ascending availability date """
        user1 = aux.createUser("foo", "foo@example.com", "example")
        availability1 = Availability.objects.get(pk=2)
        b1 = Booking.objects.book(availability1, user1)
        availability2 = Availability.objects.get(pk=1)
        b2 = Booking.objects.book(availability2, user1)
        bookingsforfoo = Booking.objects.get_by_user(user1)

        self.assertEqual(len(bookingsforfoo), 2)
        self.assertTrue(bookingsforfoo[0].availability.when < bookingsforfoo[1].availability.when)

    def test_booking_get_my_bookings_ordered_2(self):
        """ GIVEN 2 bookings for user foo; WHEN requesting bookings for user foo; THEN 2 bookings should be returned ordered by ascending availability date """
        user1 = aux.createUser("foo", "foo@example.com", "example")
        availability1 = Availability.objects.get(pk=1)
        b1 = Booking.objects.book(availability1, user1)
        availability2 = Availability.objects.get(pk=2)
        b2 = Booking.objects.book(availability2, user1)
        bookingsforfoo = Booking.objects.get_by_user(user1)

        self.assertEqual(len(bookingsforfoo), 2)
        self.assertTrue(bookingsforfoo[0].availability.when < bookingsforfoo[1].availability.when)

    def test_booking_get_my_bookings_not_cancelled(self):
        """ GIVEN 2 bookings for user foo, 1 cancelled; WHEN requesting bookings for user foo; THEN 1 bookings not cancelled should be returned """
        user1 = aux.createUser("foo", "foo@example.com", "example")
        availability1 = Availability.objects.get(pk=1)
        b1 = Booking.objects.book(availability1, user1)
        availability2 = Availability.objects.get(pk=2)
        b2 = Booking.objects.book(availability2, user1)
        b1 = b1.cancel()
        bookingsforfoo = Booking.objects.get_by_user(user1)

        self.assertEqual(len(bookingsforfoo), 1)
        self.assertFalse(bookingsforfoo[0].cancelled)

    def test_booking_cancel_1(self):
        """ GIVEN a booking, WHEN it is cancelled; THEN it is marked as cancelled """
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        booking = Booking.objects.book(availability, user)
        booking = booking.cancel()

        self.assertTrue(booking.cancelled)

    def test_booking_initially_not_cancelled(self):
        """ GIVEN a booking, WHEN ; THEN it is initially not marked as cancelled """
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        booking = Booking.objects.book(availability, user)

        self.assertFalse(booking.cancelled)

    def test_booking_cancel_2(self):
        """ GIVEN a booking, WHEN it is cancelled; THEN it's availability is freed """
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        booking = Booking.objects.book(availability, user)
        booking = booking.cancel()

        self.assertFalse(booking.availability.booked)

    def test_booking_get_by_location_and_date(self):
        """ GIVEN 2 bookings, 1 for user foo and 1 for user juan; WHEN requesting user bookings for Buenos Aires on the 2th of January 2020; THEN 1 booking with user foo should be returned """
        availability1 = Availability.objects.get(pk=1)
        user1 = aux.createUser("foo", "foo@example.com", "example")
        b1 = Booking.objects.book(availability1, user1)
        availability2 = Availability.objects.get(pk=2)
        user2 = aux.createUser("juan", "juan@example.com", "example")
        b2 = Booking.objects.book(availability2, user2)
        result = Booking.objects.get_by_location_and_date(availability1.where, datetime(2021,1,2, 0, 0, 0, 0, timezone.utc) )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].user, user1)
        self.assertEqual(result[0].availability, availability1)

    def test_booking_get_by_location_and_date_no_results(self):
        """ GIVEN 2 bookings, 1 for user foo and 1 for user juan; WHEN requesting user bookings for Buenos Aires on the 10th of January 2020; THEN 1 booking with user foo should be returned """
        availability1 = Availability.objects.get(pk=1)
        user1 = aux.createUser("foo", "foo@example.com", "example")
        b1 = Booking.objects.book(availability1, user1)
        availability2 = Availability.objects.get(pk=2)
        user2 = aux.createUser("juan", "juan@example.com", "example")
        b2 = Booking.objects.book(availability2, user2)
        result = Booking.objects.get_by_location_and_date(availability1.where, datetime(2021,1,10, 0, 0, 0, 0, timezone.utc) )

        self.assertEqual(len(result), 0)

    def test_book_availability_with_notes(self):
        """ Booking an availability with notes, saves those notes """
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        note = "Patient: Wilfredo"
        b = Booking.objects.book(availability, user, note)
        self.assertEqual(len(Booking.objects.filter(availability=availability)), 1)
        self.assertEqual(Booking.objects.filter(availability=availability)[0].user, user)
        self.assertEqual(Booking.objects.filter(availability=availability)[0].note, note)

    def test_booking_serialize_json_with_note(self):
        """ GIVEN a booking; WHEN requesting json serialization; THEN it should be returned in json format """
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        note = "Patient: Wilfredo"
        booking = Booking.objects.book(availability, user, note)

        expected_json = {'id': 1, 'availability': availability.json(), 'username': user.username, 'note': note }

        self.assertEqual(booking.json()["availability"] , expected_json["availability"])
        self.assertEqual(booking.json()["username"], expected_json["username"])
        self.assertEqual(booking.json()["note"], expected_json["note"])
