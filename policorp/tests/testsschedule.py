from django.test import TestCase
from datetime import date
from policorp.models import Booking, Availability, Location, Task
from policorp.lib.schedule import Schedule
from policorp.tests import aux

class TestSchedule(TestCase):

    fixtures = ['testsdata.json']

    def test_create_schedule_date_and_location_and_availabilities_and_bookings(self):
        """ A schedule should contain a date, a location, an array of availabilities and an array of bookings """

        today = date.today()
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
        sch = Schedule(today, l, availabilities, bookings)
        self.assertEqual(sch.date, today)
        self.assertEqual(sch.location, l)
        self.assertEqual(sch.availabilities, availabilities)
        self.assertEqual(sch.bookings, bookings)

    # TODO: Test merge operations by time

if __name__ == "__main__":
    unittest.main()
