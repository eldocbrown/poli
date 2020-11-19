from django.test import TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from policorp.models import Availability, Location, Task
import aux
import json

# Create your tests here.
class TestAvailability(TestCase):

    def test_get_availability_all(self):
        """ GIVEN 1 availability; WHEN requesting all availabilities; THEN 1 availability should be returned """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name)
        a1 = Availability.objects.create_availability(datetime.now(timezone.utc), l1, t1)
        self.assertEqual(len(Availability.objects.get_all()), 1)

    def test_get_availability_all_ordered_by_date_ascendant(self):
        """ GIVEN 3 availabilities; WHEN requesting all availabilities; THEN 3 availabilities should be returned in ascendant order by schedule date """

        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name)
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, t1)
        self.assertEqual(len(Availability.objects.get_all()), 3)
        self.assertEqual(Availability.objects.get_all()[0], a1)
        self.assertEqual(Availability.objects.get_all()[1], a2)
        self.assertEqual(Availability.objects.get_all()[2], a3)

    def test_get_availability_all_with_location(self):
        """GIVEN 1 availability at Buenos Aires, tomorrow; WHEN requesting all availabilities; THEN 1 availability should be returned at Buenos Aires, tomorrow"""

        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days = 1)
        loc_name = "Buenos Aires"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name)
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
        t1 = Task.objects.create_task(task_name)
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
        install = Task.objects.create_task("Device Installation")
        repair = Task.objects.create_task("Repair")
        now = datetime.now(timezone.utc)
        a3 = Availability.objects.create_availability(now + timedelta(days = 3), l1, install)
        a2 = Availability.objects.create_availability(now + timedelta(days = 2), l1, repair)
        a1 = Availability.objects.create_availability(now + timedelta(days = 1), l1, repair)
        self.assertEqual(len(Availability.objects.get_all_by_task(repair.name)), 2)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0], a1)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[1], a2)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[0].what, repair)
        self.assertEqual(Availability.objects.get_all_by_task(repair.name)[1].what, repair)

    def test_availability_serialize(self):
        loc_name = "Córdoba"
        l1 = Location.objects.create_location(loc_name)
        task_name = "Device Installation"
        t1 = Task.objects.create_task(task_name)
        now = datetime.now(timezone.utc)
        a1 = Availability.objects.create_availability(now + timedelta(days = 3), l1, t1)

        expected = {'id': 1, 'when': (now + timedelta(days = 3)).isoformat(), 'where': l1.json(), 'what': t1.json()}

        self.assertJSONEqual(json.dumps(a1.json()), expected)

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

class TestTask(TestCase):

    def test_get_task_all(self):
        """ GIVEN 1 task; WHEN requesting all tasks; THEN 1 task should be returned """

        task_name = "Device Installation"
        t = Task.objects.create_task(task_name)
        self.assertEqual(len(Task.objects.get_all()), 1)

    def test_get_task_all_gets_name(self):
        """ GIVEN 1 task with name "Device Installation"; WHEN requesting all tasks; THEN 1 task should be returned with name "Device Installation" """

        task_name = "Device Installation"
        t = Task.objects.create_task(task_name)
        self.assertEqual(len(Task.objects.get_all()), 1)
        self.assertEqual(Task.objects.get_all()[0].name, task_name)

    def test_task_serialize(self):
        """ GIVEN 1 task with name "Device Installation"; WHEN requesting json serialization; THEN id and name should be returned in json format """
        task_name = "Device Installation"
        t = Task.objects.create_task(task_name)
        j = {'id': 1, 'name': task_name}
        self.assertJSONEqual(json.dumps(t.json()), json.dumps(j))

class TestBooking(TestCase):

    fixtures = ['testsdata.json']

    def test_book_availability_user(self):
        availability = Availability.objects.get(pk=1)
        user = aux.createUser("foo", "foo@example.com", "example")
        b = Booking.book(availability, user)
        self.assertEqual(Booking.objects.get(pk=1).user, user)
        self.assertEqual(Booking.objects.get(pk=1).availability, availability)

if __name__ == "__main__":
    unittest.main()
