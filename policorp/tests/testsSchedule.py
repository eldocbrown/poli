from django.test import TestCase
from datetime import date
from policorp.models import Booking, Availability, Location, Task
from policorp.lib.schedule import Schedule
from policorp.tests import aux
import json

class TestSchedule(TestCase):

    maxDiff = None

    fixtures = ['testsdata.json']

    def test_create_schedule_date_and_location_and_availabilities_and_bookings(self):
        """ A schedule should contain a date, a location, an array of availabilities and an array of bookings """

        l = Location.objects.create_location('Córdoba')
        availabilities =    [
                                Availability.objects.get(pk=4),
                                Availability.objects.get(pk=6)
                            ]
        bookings =  [
                        Booking.objects.book(
                                                Availability.objects.get(pk=5),
                                                aux.createUser("foo", "foo@example.com", "example")
                                            )
                    ]
        sch = Schedule(date.today(), l, availabilities, bookings)
        self.assertEqual(sch.date, date.today())
        self.assertEqual(sch.location, l)
        self.assertEqual(sch.availabilities, availabilities)
        self.assertEqual(sch.bookings, bookings)

    def test_get_schedule_sorted_array_1(self):
        """ GIVEN a schedule; WHEN it is requested; THEN it is a sorted ascending array by date """

        l = Location.objects.create_location('Córdoba')
        availabilities =    [
                                Availability.objects.get(pk=4),
                                Availability.objects.get(pk=6)
                            ]
        bookings =  [
                        Booking.objects.book(
                                                Availability.objects.get(pk=5),
                                                aux.createUser("foo", "foo@example.com", "example")
                                            )
                    ]
        sch = Schedule(date.today(), l, availabilities, bookings)
        expected_array =    [
                                availabilities[0],
                                bookings[0],
                                availabilities[1]
                            ]
        self.assertEqual(sch.toSortedScheduleArray(), expected_array)

    def test_get_schedule_sorted_array_booking_first_when_equals(self):
        """ GIVEN a schedule; WHEN it is requested; THEN it is a sorted ascending array by date """

        availabilities =    [
                                Availability.objects.get(pk=4),
                                Availability.objects.get(pk=6)
                            ]
        user = aux.createUser("foo", "foo@example.com", "example")
        l = Location.objects.create_location('Córdoba')
        t = Task.objects.get(pk=2)
        new_availability = Availability.objects.create_availability(Availability.objects.get(pk=4).when, l, t)
        bookings =  [
                        Booking.objects.book(
                                                Availability.objects.get(pk=5),
                                                user
                                            ),
                        Booking.objects.book(
                                                new_availability,
                                                user
                                            )
                    ]
        sch = Schedule(date.today(), l, availabilities, bookings)
        expected_array =    [
                                bookings[1],
                                availabilities[0],
                                bookings[0],
                                availabilities[1]
                            ]
        self.assertEqual(sch.toSortedScheduleArray(), expected_array)

    def test_get_schedule_sorted_array_two_equal_availabilities(self):
        """ GIVEN a schedule; WHEN it is requested; THEN it is a sorted ascending array by date """

        l = Location.objects.create_location('Córdoba')
        t = Task.objects.get(pk=2)
        new_availability = Availability.objects.create_availability(Availability.objects.get(pk=4).when, l, t)
        availabilities =    [
                                Availability.objects.get(pk=4),
                                Availability.objects.get(pk=6),
                                new_availability
                            ]
        user = aux.createUser("foo", "foo@example.com", "example")
        bookings =  [
                        Booking.objects.book(
                                                Availability.objects.get(pk=5),
                                                user
                                            )
                    ]
        sch = Schedule(date.today(), l, availabilities, bookings)
        expected_array =    [
                                availabilities[0],
                                availabilities[2],
                                bookings[0],
                                availabilities[1]
                            ]
        self.assertEqual(sch.toSortedScheduleArray(), expected_array)

    def test_get_schedule_sorted_array_two_equal_bookings(self):
        """ GIVEN a schedule; WHEN it is requested; THEN it is a sorted ascending array by date """

        l = Location.objects.create_location('Córdoba')
        t = Task.objects.get(pk=2)
        new_availability = Availability.objects.create_availability(Availability.objects.get(pk=4).when, l, t)
        availabilities =    [
                                Availability.objects.get(pk=6),
                                Availability.objects.get(pk=5)
                            ]
        user = aux.createUser("foo", "foo@example.com", "example")
        bookings =  [
                        Booking.objects.book(
                                                Availability.objects.get(pk=4),
                                                user
                                            ),
                        Booking.objects.book(
                                                new_availability,
                                                user
                                            ),
                    ]
        sch = Schedule(date.today(), l, availabilities, bookings)
        expected_array =    [
                                bookings[0],
                                bookings[1],
                                availabilities[1],
                                availabilities[0]
                            ]
        self.assertEqual(sch.toSortedScheduleArray(), expected_array)

    def test_get_schedule_sorted_array_2(self):
        """ GIVEN a schedule; WHEN it is requested; THEN it is a sorted ascending array by date """

        l = Location.objects.create_location('Córdoba')
        t = Task.objects.get(pk=2)
        new_availability = Availability.objects.create_availability(Availability.objects.get(pk=4).when, l, t)
        availabilities =    [
                                Availability.objects.get(pk=5),
                                Availability.objects.get(pk=6)

                            ]
        user = aux.createUser("foo", "foo@example.com", "example")
        bookings =  [
                        Booking.objects.book(
                                                Availability.objects.get(pk=4),
                                                user
                                            )
                    ]
        sch = Schedule(date.today(), l, availabilities, bookings)
        expected_array =    [
                                bookings[0],
                                availabilities[0],
                                availabilities[1]
                            ]
        self.assertEqual(sch.toSortedScheduleArray(), expected_array)

    def test_get_schedule_sorted_json(self):
        l = Location.objects.create_location('Córdoba')
        t = Task.objects.get(pk=2)
        new_availability = Availability.objects.create_availability(Availability.objects.get(pk=4).when, l, t)
        availabilities =    [
                                Availability.objects.get(pk=6),
                                Availability.objects.get(pk=5)
                            ]
        user = aux.createUser("foo", "foo@example.com", "example")
        bookings =  [
                        Booking.objects.book(
                                                Availability.objects.get(pk=4),
                                                user
                                            ),
                        Booking.objects.book(
                                                new_availability,
                                                user
                                            ),
                    ]
        sch = Schedule(date.today(), l, availabilities, bookings)
        expected_json = {
                            'date': sch.date,
                            'location': sch.location.json(),
                            'schedule': [
                                            {'booking': bookings[0].json()},
                                            {'booking': bookings[1].json()},
                                            {'availability': availabilities[1].json()},
                                            {'availability': availabilities[0].json()}
                                        ]
                        }
        self.assertJSONEqual(json.dumps(sch.json()), json.dumps(expected_json, cls=aux.DateTimeEncoder))

    def test_get_schedule_sorted_json_2(self):
        l = Location.objects.create_location('Córdoba')
        t = Task.objects.get(pk=2)
        new_availability = Availability.objects.create_availability(Availability.objects.get(pk=4).when, l, t)
        availabilities =    [
                                Availability.objects.get(pk=5),
                                Availability.objects.get(pk=6)

                            ]
        user = aux.createUser("foo", "foo@example.com", "example")
        bookings =  [
                        Booking.objects.book(
                                                Availability.objects.get(pk=4),
                                                user
                                            )
                    ]
        sch = Schedule(date.today(), l, availabilities, bookings)
        expected_json = {
                            'date': sch.date,
                            'location': sch.location.json(),
                            'schedule': [
                                            {'booking': bookings[0].json()},
                                            {'availability': availabilities[0].json()},
                                            {'availability': availabilities[1].json()}
                                        ]
                        }
        self.assertJSONEqual(json.dumps(sch.json()), json.dumps(expected_json, cls=aux.DateTimeEncoder))


if __name__ == "__main__":
    unittest.main()
