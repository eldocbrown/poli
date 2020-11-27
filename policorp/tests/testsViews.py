from django.test import TestCase, RequestFactory, tag
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
import json
import sys
from policorp.models import Availability, Location, Task, Booking
from policorp.views import *
from policorp.tests import aux

class TestViews(TestCase):

    fixtures = ['testsdata.json']

    task1 = {'id': 1, 'name': 'Device Installation', 'duration': 120}
    task2 = {'id': 2, 'name': 'Repair', 'duration': 60}

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    @tag('tasks')
    def test_view_tasks_return_200(self):
        """ GIVEN ; WHEN GET /policorp/tasks ; THEN code 200 should be returned """
        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:tasks'))
        response = tasks(request)
        self.assertEqual(response.status_code, 200)

    @tag('tasks')
    def test_view_tasks_post_not_allowed(self):
        """ GIVEN ; WHEN POST /policorp/tasks; THEN code 400 should be returned """
        # Create an instance of a POST request.
        request = self.factory.post(reverse('policorp:tasks'))
        response = tasks(request)
        self.assertEqual(response.status_code, 400)

    @tag('tasks')
    def test_view_tasks_return_2_tasks(self):
        """ GIVEN 2 tasks with name "Device Installation" and "Repair"; WHEN GET /policorp/tasks ; THEN 2 tasks should be returned in json format """
        expected_data = [self.task1, self.task2]

        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:tasks'))
        response = tasks(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    @tag('availabilities')
    def test_view_availabilities_return_200(self):
        """ GIVEN ; WHEN GET /policorp/availabilities/1 ; THEN code 200 is returned """
        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:availabilities', kwargs={'taskid': 1}))
        response = availabilities(request, 1)
        self.assertEqual(response.status_code, 200)

    @tag('availabilities')
    def test_view_availabilities_return_1_availability(self):
        """ GIVEN ; WHEN GET /policorp/availabilities/1 ; THEN availabiliy 1 json is returned """
        expected_json = [Availability.objects.get(pk=2).json()]

        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:availabilities', kwargs={'taskid': 1}))
        response = availabilities(request, 1)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('availabilities')
    def test_view_tasks_post_not_allowed(self):
        """ GIVEN ; WHEN POST /policorp/availabilities/1; THEN code 400 is returned """
        # Create an instance of a POST request.
        request = self.factory.post(reverse('policorp:availabilities', kwargs={'taskid': 1}))
        response = availabilities(request, 1)
        self.assertEqual(response.status_code, 400)

    @tag('book')
    def test_view_book(self):
        """ GIVEN ; WHEN POST /policorp/book/1 ; THEN code 201 is returned """
        request = self.factory.post(reverse('policorp:book', kwargs={'availabilityid': 1}))
        request.user = aux.createUser("foo", "foo@example.com", "example")
        response = book(request, 1)
        self.assertEqual(response.status_code, 201)

    @tag('book')
    def test_view_book_returns_booking_json(self):
        """ GIVEN ; WHEN POST /policorp/book/1 ; THEN code 201 is returned """
        request = self.factory.post(reverse('policorp:book', kwargs={'availabilityid': 1}))
        request.user = aux.createUser("foo", "foo@example.com", "example")
        response = book(request, 1)

        expected_json = Booking.objects.get(pk=1).json()
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('book')
    def test_view_book_only_post_allowed(self):
        """ GIVEN ; WHEN GET /policorp/book/1; THEN code 400 should be returned """
        request = self.factory.get(reverse('policorp:book', kwargs={'availabilityid': 1}))
        request.user = AnonymousUser()
        response = book(request, 1)
        self.assertEqual(response.status_code, 400)

    @tag('book')
    def test_view_book_only_logged_in_requests_allowed(self):
        """ GIVEN ; WHEN POST /policorp/book/1 logged out; THEN code 401 (unauthorized) should be returned """
        request = self.factory.post(reverse('policorp:book', kwargs={'availabilityid': 1}))
        request.user = AnonymousUser()
        response = book(request, 1)
        self.assertEqual(response.status_code, 401)

    @tag('myschedule')
    def test_view_myschedule_returns_200(self):
        """ GIVEN ; WHEN GET /myschedule ; THEN code 200 is returned """
        request = self.factory.get(reverse('policorp:myschedule'))
        request.user = aux.createUser('foo', 'foo@example.com', 'example')
        response = myschedule(request)
        self.assertEqual(response.status_code, 200)

    @tag('myschedule')
    def test_view_myschedule_post_not_allowed(self):
        """ GIVEN ; WHEN POST /myschedule; THEN code 400 should be returned """
        # Create an instance of a POST request.
        request = self.factory.post(reverse('policorp:myschedule'))
        response = myschedule(request)
        self.assertEqual(response.status_code, 400)

    @tag('myschedule')
    def test_view_myschedule_only_logged_in_requests_allowed(self):
        """ GIVEN ; WHEN GET /myschedule logged out; THEN code 401 (unauthorized) should be returned """
        request = self.factory.get(reverse('policorp:myschedule'))
        request.user = AnonymousUser()
        response = myschedule(request)
        self.assertEqual(response.status_code, 401)

    @tag('myschedule')
    def test_view_myschedule_returns_caller_bookings(self):
        """ GIVEN 2 bookings for user foo; WHEN GET /myschedule with user foo; THEN json with 2 bookings should be returned"""
        user1 = aux.createUser("foo", "foo@example.com", "example")
        availability1 = Availability.objects.get(pk=1)
        b1 = Booking.objects.book(availability1, user1)
        availability2 = Availability.objects.get(pk=2)
        b2 = Booking.objects.book(availability2, user1)
        request = self.factory.get(reverse('policorp:myschedule'))
        request.user = user1
        response = myschedule(request)

        expected_json = [b1.json(), b2.json()]
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('cancelbooking')
    def test_view_cancelbooking(self):
        """ GIVEN a booking for user foo; WHEN POST /policorp/cancelbooking/1 ; THEN code 201 is returned """
        user1 = aux.createUser("foo", "foo@example.com", "example")
        availability1 = Availability.objects.get(pk=1)
        b1 = Booking.objects.book(availability1, user1)
        request = self.factory.post(reverse('policorp:cancelbooking', kwargs={'bookingid': 1}))
        request.user = user1
        response = cancelbooking(request, 1)
        self.assertEqual(response.status_code, 201)

    @tag('cancelbooking')
    def test_view_cancelbooking_only_post_allowed(self):
        """ GIVEN ; WHEN GET /policorp/cancelbooking/1; THEN code 400 should be returned """
        request = self.factory.get(reverse('policorp:cancelbooking', kwargs={'bookingid': 1}))
        request.user = AnonymousUser()
        response = cancelbooking(request, 1)
        self.assertEqual(response.status_code, 400)

    @tag('cancelbooking')
    def test_view_cancelbooking_only_logged_in_requests_allowed(self):
        """ GIVEN ; WHEN POST /policorp/cancelbooking/1 logged out; THEN code 401 (unauthorized) should be returned """
        request = self.factory.post(reverse('policorp:cancelbooking', kwargs={'bookingid': 1}))
        request.user = AnonymousUser()
        response = cancelbooking(request, 1)
        self.assertEqual(response.status_code, 401)

    @tag('cancelbooking')
    def test_view_cancelbooking_only_user_in_booking_allowed(self):
        """ GIVEN a booking for user foo; WHEN POST /policorp/cancelbooking/1 logged in with user zoe; THEN code 401 (unauthorized) should be returned """
        user1 = aux.createUser("foo", "foo@example.com", "example")
        availability1 = Availability.objects.get(pk=1)
        b1 = Booking.objects.book(availability1, user1)
        user2 = aux.createUser("zoe", "zoe@example.com", "example")
        request = self.factory.post(reverse('policorp:cancelbooking', kwargs={'bookingid': 1}))
        request.user = user2
        response = cancelbooking(request, 1)
        self.assertEqual(response.status_code, 401)

    @tag('cancelbooking')
    def test_view_cancelbooking_returns_cancelled_booking(self):
        """ GIVEN a booking for user foo; WHEN POST /cancelbooking with user foo; THEN json with 2 bookings should be returned"""
        user1 = aux.createUser("foo", "foo@example.com", "example")
        availability1 = Availability.objects.get(pk=1)
        b1 = Booking.objects.book(availability1, user1)

        request = self.factory.post(reverse('policorp:cancelbooking', kwargs={'bookingid': 1}))
        request.user = user1
        response = cancelbooking(request, 1)

        expected_json = Booking.objects.get(pk=1).json()
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('mysupervisedlocations')
    def test_view_mysupervisedlocations_returns_200(self):
        """ GIVEN; WHEN GET /mysupervisedlocation; THEN status code 200 is returned """
        request = self.factory.get(reverse('policorp:mysupervisedlocations'))
        request.user = aux.createUser('foo', 'foo@example.com', 'example')
        response = mysupervisedlocations(request)
        self.assertEqual(response.status_code, 200)

    @tag('mysupervisedlocations')
    def test_view_mysupervisedlocations_post_not_allowed(self):
        """ GIVEN ; WHEN POST /mysupervisedlocations; THEN code 400 should be returned """
        # Create an instance of a POST request.
        request = self.factory.post(reverse('policorp:mysupervisedlocations'))
        response = mysupervisedlocations(request)
        self.assertEqual(response.status_code, 400)

    @tag('mysupervisedlocations')
    def test_view_mysupervisedlocations_only_logged_in_requests_allowed(self):
        """ GIVEN ; WHEN GET /mysupervisedlocations logged out; THEN code 401 (unauthorized) should be returned """
        request = self.factory.get(reverse('policorp:mysupervisedlocations'))
        request.user = AnonymousUser()
        response = mysupervisedlocations(request)
        self.assertEqual(response.status_code, 401)

    @tag('mysupervisedlocations')
    def test_view_mysupervisedlocations_returns_locations(self):
        """ GIVEN user foo that supervises a location; WHEN GET /mysupervisedlocation with user foo; THEN json with that location should be returned """
        user = aux.createUser('foo', 'foo@example.com', 'example')
        location = Location.objects.get(pk=1)
        location.assign_supervisor(user)
        request = self.factory.get(reverse('policorp:mysupervisedlocations'))
        request.user = user
        response = mysupervisedlocations(request)

        expected_json = [location.json()]
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('mysupervisedlocations')
    def test_view_mysupervisedlocations_returns_locations_2(self):
        """ GIVEN user foo that supervises a location and user juan that supervises another location; WHEN GET /mysupervisedlocation with user foo; THEN json with that 1 location should be returned """
        user = aux.createUser('foo', 'foo@example.com', 'example')
        user2 = aux.createUser('juan', 'juan@example.com', 'example')
        location = Location.objects.get(pk=1)
        location2 = Location.objects.get(pk=2)
        location.assign_supervisor(user)
        location2.assign_supervisor(user2)
        request = self.factory.get(reverse('policorp:mysupervisedlocations'))
        request.user = user
        response = mysupervisedlocations(request)

        expected_json = [location.json()]
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('mysupervisedlocations')
    def test_view_mysupervisedlocations_returns_locations_3(self):
        """ GIVEN user foo that supervises 2 locations and user juan that supervises another location; WHEN GET /mysupervisedlocation with user foo; THEN json with 2 locations should be returned """
        user = aux.createUser('foo', 'foo@example.com', 'example')
        user2 = aux.createUser('juan', 'juan@example.com', 'example')
        location = Location.objects.get(pk=1)
        location2 = Location.objects.get(pk=2)
        location3 = Location.objects.get(pk=3)
        location.assign_supervisor(user)
        location3.assign_supervisor(user)
        location2.assign_supervisor(user2)
        request = self.factory.get(reverse('policorp:mysupervisedlocations'))
        request.user = user
        response = mysupervisedlocations(request)

        expected_json = [location.json(), location3.json()]
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('mysupervisedlocations')
    def test_view_mysupervisedlocations_returns_locations_ordered(self):
        """ GIVEN user foo that supervises 3 locations; WHEN GET /mysupervisedlocation with user foo; THEN json with 2 locations should be returned ordered ascending by location name """
        user = aux.createUser('foo', 'foo@example.com', 'example')
        locationBA = Location.objects.filter(name="Buenos Aires").first()
        locationC = Location.objects.filter(name="Córdoba").first()
        locationR = Location.objects.filter(name="Rosario").first()
        locationC.assign_supervisor(user)
        locationBA.assign_supervisor(user)
        locationR.assign_supervisor(user)
        request = self.factory.get(reverse('policorp:mysupervisedlocations'))
        request.user = user
        response = mysupervisedlocations(request)

        expected_json = [locationBA.json(), locationC.json(), locationR.json()]
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

if __name__ == "__main__":
    unittest.main()
