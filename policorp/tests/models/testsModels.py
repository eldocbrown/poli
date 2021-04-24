from django.test import TestCase
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from policorp.models import Availability, Location, Task, Booking, User
from policorp.tests import aux
import json

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
        self.assertEqual(t.json()["name"], j["name"])
        self.assertEqual(t.json()["duration"], j["duration"])

    def test_task_duration(self):
        """ GIVEN ; WHEN creating a task; THEN a duration in minutes must be provided """
        task_name = "Device Installation"
        t = Task.objects.create_task(task_name, 30)
        self.assertEqual(Task.objects.get(name=task_name).duration, 30)

    def test_task_duration_not_negative(self):
        """ GIVEN ; WHEN creating a task with negative duration; THEN an exception must be raised """
        task_name = "Device Installation"
        with self.assertRaises(IntegrityError):
            Task.objects.create_task(task_name, -30)

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
