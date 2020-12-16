from django.test import TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from policorp.models import Availability, Location, Task, Booking, User
from policorp.tests import aux
import json

# Create your tests here.
class TestAvailability(TestCase):

    def test_get_availability_all(self):
        """ GIVEN 1 availability; WHEN requesting all availabilities; THEN 1 availability should be returned """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(datetime.now(timezone.utc), l1, t1)
        self.assertEqual(len(Availability.objects.get_all()), 1)

    def test_get_availability_all_ordered_by_date_ascendant(self):
        """ GIVEN 3 availabilities; WHEN requesting all availabilities; THEN 3 availabilities should be returned in ascendant order by schedule date """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, t1)
        self.assertEqual(len(Availability.objects.get_all()), 3)
        self.assertEqual(Availability.objects.get_all()[0], a1)
        self.assertEqual(Availability.objects.get_all()[1], a2)
        self.assertEqual(Availability.objects.get_all()[2], a3)

    def test_get_availability_all_ordered_by_date_ascendant(self):
        """ GIVEN 3 availabilities, 1 booked; WHEN requesting all availabilities; THEN 2 availabilities should be returned in ascendant order by schedule date """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, t1)
        a2.book()
        self.assertEqual(len(Availability.objects.get_all()), 2)
        self.assertIn(a1, Availability.objects.get_all())
        self.assertIn(a3, Availability.objects.get_all())
        self.assertTrue(Availability.objects.get_all()[0].when < Availability.objects.get_all()[1].when)

    def test_get_availability_all_with_location(self):
        """GIVEN 1 availability at Buenos Aires, tomorrow; WHEN requesting all availabilities; THEN 1 availability should be returned at Buenos Aires, tomorrow"""

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)
        self.assertEqual(len(Availability.objects.get_all()), 1)
        availability = Availability.objects.get_all()[0]
        self.assertEqual(availability.when, tomorrow)
        self.assertEqual(availability.where.name, loc_name)

    def test_get_availability_all_by_task(self):
        """ GIVEN 1 availability at Cordoba, tomorrow, for "Device Installation", WHEN requesting all availabilities for "Device Installation", THEN 1 availability should be returned at Cordoba, tomorrow for "Device Installation" """

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)
        self.assertEqual(len(Availability.objects.get_all_by_task(task_name)), 1)
        availability = Availability.objects.get_all_by_task(task_name)[0]
        self.assertEqual(availability.when, tomorrow)
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_all_by_task_ordered_by_date_ascendant(self):
        """ GIVEN 3 availabilities, 1 for Device Installation, 2 for Repair; WHEN requesting all availabilities for "Repair"; THEN 2 availabilities should be returned in ascendant order by schedule date for task "Repair" """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        install = Task.objects.create_task("Device Installation", 30)
        repair = Task.objects.create_task("Repair", 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, install)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, repair)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, repair)
        self.assertEqual(len(Availability.objects.get_all_by_task(repair.name)), 2)
        self.assertIn(a1, Availability.objects.get_all_by_task(repair.name))
        self.assertIn(a2, Availability.objects.get_all_by_task(repair.name))
        self.assertTrue(Availability.objects.get_all_by_task(repair.name)[0].when < Availability.objects.get_all_by_task(repair.name)[1].when)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0].what, repair)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[1].what, repair)

    def test_get_availability_all_by_task_ordered_by_date_ascendant_2(self):
        """ GIVEN 3 availabilities, 1 for Device Installation, 2 for Repair; WHEN requesting all availabilities for "Repair"; THEN 2 availabilities should be returned in ascendant order by schedule date for task "Repair" """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        install = Task.objects.create_task("Device Installation", 30)
        repair = Task.objects.create_task("Repair", 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, install)
        a2 = Availability.objects.create_availability(now + timedelta(days = 1), l1, repair)
        a1 = Availability.objects.create_availability(now + timedelta(days = 2), l1, repair)
        self.assertEqual(len(Availability.objects.get_all_by_task(repair.name)), 2)
        self.assertIn(a1, Availability.objects.get_all_by_task(repair.name))
        self.assertIn(a2, Availability.objects.get_all_by_task(repair.name))
        self.assertTrue(Availability.objects.get_all_by_task(repair.name)[0].when < Availability.objects.get_all_by_task(repair.name)[1].when)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0].what, repair)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[1].what, repair)

    def test_get_availability_all_by_task_ordered_by_date_ascendant(self):
        """ GIVEN 3 availabilities, 1 for Device Installation, 2 for Repair, 1 Repair is boooked; WHEN requesting all availabilities for "Repair"; THEN 1 availabilities should be returned in ascendant order by schedule date for task "Repair" """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        install = Task.objects.create_task("Device Installation", 30)
        repair = Task.objects.create_task("Repair", 30)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, install)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, repair)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, repair)
        a1.book()
        self.assertEqual(len(Availability.objects.get_all_by_task(repair.name)), 1)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0], a2)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0].what, repair)

    def test_availability_serialize(self):
        loc_name = "Córdoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a1 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)

        expected = {'id': 1, 'when': (now + timedelta(days = 3)).isoformat(), 'where': l1.json(), 'what': t1.json()}

        self.assertJSONEqual(json.dumps(a1.json()), expected)

    def test_availability_booked_initially_false(self):
        """ New availability should be not booked by default """
        loc_name = "Córdoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a1 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)

        self.assertFalse(a1.booked)

    def test_availability_book(self):
        """ Given an availabiliy, when booked, then it is marked as booked """
        loc_name = "Córdoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a1 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)
        a1.book()

        self.assertTrue(a1.booked)

    def test_availability_free(self):
        """ GIVEN a booked availabiliy; WHEN freed; THEN it is marked as not booked """
        loc_name = "Córdoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        now = datetime.now(timezone.utc)
        a1 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)
        a1.book()
        self.assertTrue(a1.booked)
        a1.free()
        self.assertFalse(a1.booked)

    def test_get_availability_next_by_task_and_date(self):
        """ GIVEN 1 availability at Cordoba, tomorrow, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for tomorrow, THEN 1 availability should be returned at Cordoba, tomorrow for "Device Installation" """

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow, l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, tomorrow)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, tomorrow)
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_no_availabilities_at_date(self):
        """ GIVEN 1 availability at Cordoba, tomorrow + 1, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 0 availability should be returned """

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 30)
        a1 = Availability.objects.create_availability(tomorrow + timedelta(days = 1), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, tomorrow)
        self.assertEqual(len(result), 0)

    def test_get_availability_next_by_task_and_date_no_more_availabilities_today(self):
        """ GIVEN 1 availability at Cordoba, now - 30min, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 0 availability should be returned """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = -30), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, now)
        self.assertEqual(len(result), 0)

    def test_get_availability_next_by_task_and_date_1_availability_today(self):
        """ GIVEN 1 availability at Cordoba, now + 30min, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 1 availability should be returned """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 30), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, now)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(minutes = 30))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_2_availability_today_ordered_ascending(self):
        """ GIVEN 2 availabilities at Cordoba, now + 30min and now + 60min, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 2 availabilities should be returned """

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 60), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = 30), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, now)
        self.assertEqual(len(result), 2)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(minutes = 30))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)
        availability = result[1]
        self.assertEqual(availability.when, now + timedelta(minutes = 60))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

    def test_get_availability_next_by_task_and_date_1_availability_today2(self):
        """ GIVEN 2 availabilities at Cordoba, now + 30min and now - 60min, for "Device Installation"; WHEN requesting next availabilities for "Device Installation" for today, THEN 1 availability should be returned for now + 30min"""

        now = datetime.now(timezone.utc)
        loc_name = "Cordoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name, 60)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 30), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = -60), l1, t1)
        result = Availability.objects.get_next_by_task_and_date(task_name, now)
        self.assertEqual(len(result), 1)
        availability = result[0]
        self.assertEqual(availability.when, now + timedelta(minutes = 30))
        self.assertEqual(availability.where.name, loc_name)
        self.assertEqual(availability.what.name, task_name)

class TestLocation(TestCase):

    fixtures = ['testsdata.json']

    loc1 = "Buenos Aires"
    loc2 = "Córdoba"
    loc3 = "Rosario"

    def test_get_location_all(self):
        """ GIVEN 3 locations; WHEN requesting all locations; THEN 3 locations should be returned """

        self.assertEqual(len(Location.objects.get_all()), 3)

    def test_get_location_all_gets_name(self):
        """ GIVEN 3 locations; WHEN requesting all locations; THEN location names should be returned """

        self.assertEqual(Location.objects.get_all()[0].name, self.loc1)
        self.assertEqual(Location.objects.get_all()[1].name, self.loc2)
        self.assertEqual(Location.objects.get_all()[2].name, self.loc3)

    def test_location_serialize(self):
        """ GIVEN 3 locations; WHEN requesting json serialization; THEN id and name should be returned in json format """
        l1 = Location.objects.get(pk=1)
        expected = {'id': 1, 'name': self.loc1}
        self.assertJSONEqual(json.dumps(l1.json()), expected)

    def test_location_supervisor(self):
        """ GIVEN 1 location; WHEN assigning a supervisor; THEN a user is saved in supervisors field """
        l1 = Location.objects.get(pk=1)
        u = User.objects.create_supervisor("foo", "foo@example.com", "example")
        l1.assign_supervisor(u)
        l1 = Location.objects.get(pk=1)
        self.assertIn(u, l1.supervisors.all())

    def test_location_supervisor_twice(self):
        """ GIVEN 1 location with an assigned supervisor; WHEN assigning a supervisor twice; THEN an exception occurs """
        l1 = Location.objects.get(pk=1)
        u = User.objects.create_supervisor("foo", "foo@example.com", "example")
        l1.assign_supervisor(u)
        with self.assertRaises(ValidationError):
            l1.assign_supervisor(u)

    def test_location_supervisor_user_is_not_supervisor_error(self):
        """ GIVEN 1 location; WHEN assigning a consumer user; THEN a ValidationError is raised """
        l1 = Location.objects.get(pk=1)
        u = aux.createUser("foo", "foo@example.com", "example")
        with self.assertRaises(ValidationError):
            l1.assign_supervisor(u)

    def test_location_remove_supervisor(self):
        """ GIVEN 1 location with an assigned supervisor; WHEN removing that supervisor; THEN the user is removed from supervisors field """
        l1 = Location.objects.get(pk=1)
        u = User.objects.create_supervisor("foo", "foo@example.com", "example")
        l1.assign_supervisor(u)
        l1 = Location.objects.get(pk=1)
        self.assertIn(u, l1.supervisors.all())
        l1.remove_supervisor(u)
        self.assertNotIn(u, l1.supervisors.all())

    def test_location_remove_not_existant_supervisor(self):
        """ GIVEN 1 location; WHEN removing a not assigned supervisor; THEN an exception is raised """
        l1 = Location.objects.get(pk=1)
        u = User.objects.create_supervisor("foo", "foo@example.com", "example")
        with self.assertRaises(ValidationError):
            l1.remove_supervisor(u)

    def test_get_supervised_locations(self):
        """ GIVEN a user supervising a location; WHEN I request all supervised locations for user; THEN location is in returned array """
        user = User.objects.create_supervisor("foo", "foo@example.com", "example")
        location = Location.objects.get(pk=1)
        location.assign_supervisor(user)
        self.assertIn(location, user.supervisedLocations.all())

    def test_get_supervised_locations_not_included(self):
        """ GIVEN a user not supervising a location; WHEN I request all supervised locations for user; THEN location is not in returned array """
        user = User.objects.create_supervisor("foo", "foo@example.com", "example")
        location = Location.objects.get(pk=1)
        self.assertNotIn(location, user.supervisedLocations.all())

class TestTask(TestCase):

    def test_get_task_all(self):
        """ GIVEN 1 task; WHEN requesting all tasks; THEN 1 task should be returned """
        task_name = "Device Installation"
        t = Task.objects.create_task(task_name, 30)
        self.assertEqual(len(Task.objects.get_all()), 1)

    def test_get_task_all_gets_name(self):
        """ GIVEN 1 task with name "Device Installation"; WHEN requesting all tasks; THEN 1 task should be returned with name "Device Installation" """
        task_name = "Device Installation"
        t = Task.objects.create_task(task_name, 15)
        self.assertEqual(len(Task.objects.get_all()), 1)
        self.assertEqual(Task.objects.get_all()[0].name, task_name)

    def test_task_serialize_json(self):
        """ GIVEN 1 task with name "Device Installation"; WHEN requesting json serialization; THEN id and name should be returned in json format """
        task_name = "Device Installation"
        duration = 60
        t = Task.objects.create_task(task_name, duration)
        j = {'id': 1, 'name': task_name, 'duration': duration}
        self.assertJSONEqual(json.dumps(t.json()), json.dumps(j))

    def test_task_duration(self):
        """ GIVEN ; WHEN creating a task; THEN a duration in minutes must be provided """
        task_name = "Device Installation"
        t = Task.objects.create_task(task_name, 30)
        self.assertEqual(Task.objects.get(pk=1).duration, 30)

    def test_task_duration_not_negative(self):
        """ GIVEN ; WHEN creating a task with negative duration; THEN an exception must be raised """
        task_name = "Device Installation"
        with self.assertRaises(IntegrityError):
            Task.objects.create_task(task_name, -30)

class TestBooking(TestCase):

    fixtures = ['testsdata.json']

    def test_book_availability_user(self):
        """ Booking an availability registers who boooked it """
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        b = Booking.objects.book(availability, user)
        self.assertEqual(Booking.objects.get(pk=1).user, user)
        self.assertEqual(Booking.objects.get(pk=1).availability, availability)

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

        expected_json = {'id': 1, 'availability': availability.json(), 'username': user.username}

        self.assertJSONEqual(json.dumps(booking.json()), json.dumps(expected_json))

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

    def test_booking_cancel(self):
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

    def test_booking_cancel(self):
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

class TestUser(TestCase):

    def test_user_is_supervisor_false_default(self):
        """ GIVEN ; WHEN creating a consumer user; THEN it is not supervisor by default """
        u = User()
        u.username = "foo"
        u.email = "foo@example.com"
        u.set_password("example")
        u.save()
        u = User.objects.get(username="foo")
        self.assertFalse(u.is_supervisor)

    def test_user_create_supervisor(self):
        """ GIVEN ; WHEN creating a supervisor user; THEN it is supervisor """
        u = User.objects.create_supervisor("foo", "foo@example.com", "example")
        u = User.objects.filter(username="foo").first()
        self.assertTrue(u.is_supervisor)

if __name__ == "__main__":
    unittest.main()
