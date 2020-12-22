from django.test import TestCase, RequestFactory, tag
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
import json
import sys
from policorp.models import Availability, Location, Task, Booking
from policorp.views import *
from policorp.tests import aux
from datetime import datetime, timedelta
import logging

class TestViews(TestCase):

    fixtures = ['testsdata.json']

    task1 = {'id': 1, 'name': 'Device Installation', 'duration': 120}
    task2 = {'id': 2, 'name': 'Repair', 'duration': 60}

    maxDiff = None

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
    def test_view_availabilities_return_2_availabilities(self):
        """ GIVEN 2 availabilities for task 3; WHEN GET /policorp/availabilities/3 ; THEN 2 json availabilities are returned """
        now = datetime.now(timezone.utc)
        l1 = Location.objects.get(pk=1)
        task_name = "Device Installation for Trucks"
        t1 = Task.objects.create_task(task_name, 120)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 60), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = 30), l1, t1)

        expected_json = [a2.json(), a1.json()]

        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:availabilities', kwargs={'taskid': t1.id}))
        response = availabilities(request, t1.id)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('availabilities')
    def test_view_availabilities_return_1_availability_today(self):
        """ GIVEN 2 availabilities for task 3, location 1 for today, now + 30min and now - 60min; WHEN GET /policorp/availabilities/1 ; THEN availabiliy 1 json availabilities is returned, now + 30 """
        now = datetime.now(timezone.utc)
        l1 = Location.objects.get(pk=1)
        task_name = "Device Installation for Trucks"
        t1 = Task.objects.create_task(task_name, 120)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 30), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = -60), l1, t1)

        expected_json = [a1.json()]

        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:availabilities', kwargs={'taskid': t1.id}))
        response = availabilities(request, t1.id)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('availabilities')
    def test_view_availabilities_return_1_availability_tomorrow(self):
        """ GIVEN 2 availabilities for task 3, location 1 for today, now - 30min and tomorrow - 60min; WHEN GET /policorp/availabilities/1 ; THEN availabiliy 1 json availabilities is returned, tomorrow - 60 """
        now = datetime.now(timezone.utc)
        l1 = Location.objects.get(pk=1)
        task_name = "Device Installation for Trucks"
        t1 = Task.objects.create_task(task_name, 120)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = -30), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(days=1,minutes = -60), l1, t1)

        expected_json = [a2.json()]

        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:availabilities', kwargs={'taskid': t1.id}))
        response = availabilities(request, t1.id)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('availabilities')
    def test_view_availabilities_post_not_allowed(self):
        """ GIVEN ; WHEN POST /policorp/availabilities/1; THEN code 400 is returned """
        # Create an instance of a POST request.
        request = self.factory.post(reverse('policorp:availabilities', kwargs={'taskid': 1}))
        response = availabilities(request, 1)
        self.assertEqual(response.status_code, 400)

    @tag('dailyavailabilities')
    def test_view_dailyavailabilities_return_200(self):
        """ GIVEN ; WHEN GET /policorp/dailyavailabilities/1/20200101 ; THEN code 200 is returned """
        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:dailyavailabilities', kwargs={'taskid': 1, 'date': '20200101'}))
        response = dailyavailabilities(request, 1, '20200101')
        self.assertEqual(response.status_code, 200)

    @tag('dailyavailabilities')
    def test_view_dailyavailabilities_post_not_allowed(self):
        """ GIVEN ; WHEN POST /policorp/dailyavailabilities/1/20200101; THEN code 400 is returned """
        # Create an instance of a POST request.
        request = self.factory.post(reverse('policorp:dailyavailabilities', kwargs={'taskid': 1, 'date': '20200101'}))
        response = dailyavailabilities(request, 1, '20200101')
        self.assertEqual(response.status_code, 400)

    @tag('dailyavailabilities')
    def test_view_dailyavailabilities_return_1_availability_today(self):
        """ GIVEN 2 availabilities for task 3, location 1 for today, now + 30min and now - 60min; WHEN GET /policorp/availabilities/1/[today] ; THEN availabiliy 1 json availabilities is returned, now + 30 """
        now = datetime.now(timezone.utc)
        l1 = Location.objects.get(pk=1)
        task_name = "Device Installation for Trucks"
        t1 = Task.objects.create_task(task_name, 120)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 30), l1, t1)
        a2 = Availability.objects.create_availability(now + timedelta(minutes = -60), l1, t1)

        expected_json = [a1.json()]

        # Create an instance of a GET request.
        datestr = now.date().isoformat().replace('-','')
        request = self.factory.get(reverse('policorp:dailyavailabilities', kwargs={'taskid': t1.id, 'date': datestr}))
        response = dailyavailabilities(request, t1.id, datestr)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('dailyavailabilities')
    def test_view_dailyavailabilities_return_2_availabilities(self):
        """ GIVEN 2 availabilities for task 3; WHEN GET /policorp/dailyavailabilities/3/[tomorrow] ; THEN 2 json availabilities are returned """
        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days=1)
        l1 = Location.objects.get(pk=1)
        task_name = "Device Installation for Trucks"
        t1 = Task.objects.create_task(task_name, 120)
        a1 = Availability.objects.create_availability(tomorrow + timedelta(minutes = 60), l1, t1)
        a2 = Availability.objects.create_availability(tomorrow + timedelta(minutes = 30), l1, t1)

        expected_json = [a2.json(), a1.json()]

        # Create an instance of a GET request.
        datestr = tomorrow.date().isoformat().replace('-','')
        request = self.factory.get(reverse('policorp:dailyavailabilities', kwargs={'taskid': t1.id, 'date': datestr}))
        response = dailyavailabilities(request, t1.id, datestr)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

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
        request.user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
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
    def test_view_mysupervisedlocations_only_logged_in_supervisors_requests_allowed(self):
        """ GIVEN ; WHEN GET /mysupervisedlocations logged in with a consumer user; THEN code 401 (unauthorized) should be returned """
        request = self.factory.get(reverse('policorp:mysupervisedlocations'))
        request.user = aux.createUser('foo', 'foo@example.com', 'example')
        response = mysupervisedlocations(request)
        self.assertEqual(response.status_code, 401)

    @tag('mysupervisedlocations')
    def test_view_mysupervisedlocations_returns_locations(self):
        """ GIVEN user foo that supervises a location; WHEN GET /mysupervisedlocation with user foo; THEN json with that location should be returned """
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
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
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        user2 = User.objects.create_supervisor('juan', 'juan@example.com', 'example')
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
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        user2 = User.objects.create_supervisor('juan', 'juan@example.com', 'example')
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
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
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

    @tag('mysupervisedlocations')
    def test_view_mysupervisedlocations_returns_locations_ordered_2(self):
        """ GIVEN user foo that supervises 3 locations; WHEN GET /mysupervisedlocation with user foo; THEN json with 2 locations should be returned ordered ascending by location name """
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        locationBA = Location.objects.filter(name="Buenos Aires").first()
        locationC = Location.objects.filter(name="Córdoba").first()
        locationR = Location.objects.filter(name="Rosario").first()
        locationR.assign_supervisor(user)
        locationC.assign_supervisor(user)
        locationBA.assign_supervisor(user)
        request = self.factory.get(reverse('policorp:mysupervisedlocations'))
        request.user = user
        response = mysupervisedlocations(request)

        expected_json = [locationBA.json(), locationC.json(), locationR.json()]
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('locationschedule')
    def test_view_locationschedule_returns_200(self):
        """ GIVEN; WHEN GET /locationschedule/1/20210102; THEN status code 200 is returned """
        request = self.factory.get(reverse('policorp:locationschedule', kwargs={'locationid': 1, 'date': '20210102'}))
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        request.user = user
        Location.objects.get(pk=1).assign_supervisor(user)
        response = locationschedule(request, 1, '20210102')
        self.assertEqual(response.status_code, 200)

    @tag('locationschedule')
    def test_view_locationschedule_post_not_allowed(self):
        """ GIVEN ; WHEN POST /locationschedule/1/20210102; THEN code 400 should be returned """
        # Create an instance of a POST request.
        request = self.factory.post(reverse('policorp:locationschedule', kwargs={'locationid': 1, 'date': '20210102'}))
        response = locationschedule(request, 1, '20210102')
        self.assertEqual(response.status_code, 400)

    @tag('locationschedule')
    def test_view_locationschedule_only_logged_in_requests_allowed(self):
        """ GIVEN ; WHEN GET /locationschedule/1/20210102 logged out; THEN code 401 (unauthorized) should be returned """
        request = self.factory.get(reverse('policorp:locationschedule', kwargs={'locationid': 1, 'date': '20210102'}))
        request.user = AnonymousUser()
        response = locationschedule(request, 1, '20210102')
        self.assertEqual(response.status_code, 401)

    @tag('locationschedule')
    def test_view_locationschedule_only_logged_in_rolepervisor_requests_allowed(self):
        """ GIVEN ; WHEN GET /locationschedule/1/20210102 logged in with a non supervisor user; THEN code 401 (unauthorized) should be returned """
        request = self.factory.get(reverse('policorp:locationschedule', kwargs={'locationid': 1, 'date': '20210102'}))
        request.user = aux.createUser('foo', 'foo@example.com', 'example')
        response = locationschedule(request, 1, '20210102')
        self.assertEqual(response.status_code, 401)

    @tag('locationschedule')
    def test_view_locationschedule_only_requests_for_supervised_locations_allowed(self):
        """ GIVEN ; WHEN GET /locationschedule/1/20210102 for a location not supervised; THEN code 401 (unauthorized) should be returned """
        request = self.factory.get(reverse('policorp:locationschedule', kwargs={'locationid': 1, 'date': '20210102'}))
        request.user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        response = locationschedule(request, 1, '20210102')
        self.assertEqual(response.status_code, 401)

    @tag('locationschedule')
    def test_view_locationschedule_return_1_booking(self):
        """ GIVEN 1 booking for 2021-01-02 at location 1; WHEN requesting schedule for 2021-01-02 at location 1; 1 json object is returned """
        request = self.factory.get(reverse('policorp:locationschedule', kwargs={'locationid': 1, 'date': '20210102'}))
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        request.user = user
        location = Location.objects.get(pk=1)
        location.assign_supervisor(user)
        booking = Booking.objects.book(Availability.objects.get(pk=1), aux.createUser('bar', 'bar@example.com', 'example'))
        response = locationschedule(request, 1, '20210102')
        expected_data = {
                            'date': '2021-01-02',
                            'location': location.json(),
                            'schedule': [
                                            {"booking": Booking.objects.get(id=booking.id).json()},
                                        ]
                        }
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    @tag('locationschedule')
    def test_view_locationschedule_return_1_booking_2(self):
        """ GIVEN 2 booking for 2021-01-02 and 2021-01-03 at location 3; WHEN requesting schedule for 2021-01-02 at location 1; 1 json object is returned """
        request = self.factory.get(reverse('policorp:locationschedule', kwargs={'locationid': 3, 'date': '20210102'}))
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        request.user = user
        location = Location.objects.get(pk=3)
        location.assign_supervisor(user)
        booker = aux.createUser('bar', 'bar@example.com', 'example')
        booking3 = Booking.objects.book(Availability.objects.get(pk=3), booker)
        booking2 = Booking.objects.book(Availability.objects.get(pk=2), booker)
        response = locationschedule(request, 3, '20210102')
        expected_data = {
                            'date': '2021-01-02',
                            'location': location.json(),
                            'schedule': [
                                            {"booking": Booking.objects.get(id=booking3.id).json()},
                                        ]
                        }
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    @tag('locationschedule')
    def test_view_locationschedule_return_1_booking_ordered_ascending(self):
        """ GIVEN 3 booking for 2021-01-04 at location 2; WHEN requesting schedule for 2021-01-04 at location 2; 3 json objects are returned in ascending order """
        request = self.factory.get(reverse('policorp:locationschedule', kwargs={'locationid': 2, 'date': '20210104'}))
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        request.user = user
        location = Location.objects.get(pk=2)
        location.assign_supervisor(user)
        booker4 = aux.createUser('bar', 'bar@example.com', 'example')
        booker5 = aux.createUser('zoe', 'zoe@example.com', 'example')
        booker6 = aux.createUser('kari', 'kari@example.com', 'example')
        booking5 = Booking.objects.book(Availability.objects.get(pk=5), booker5)
        booking6 = Booking.objects.book(Availability.objects.get(pk=6), booker6)
        booking4 = Booking.objects.book(Availability.objects.get(pk=4), booker4)
        response = locationschedule(request, 2, '20210104')
        expected_data = [Booking.objects.get(id=booking4.id).json(), Booking.objects.get(id=booking5.id).json(), Booking.objects.get(id=booking6.id).json()]
        expected_data = {
                            'date': '2021-01-04',
                            'location': location.json(),
                            'schedule': [
                                            {"booking": Booking.objects.get(id=booking4.id).json()},
                                            {"booking": Booking.objects.get(id=booking5.id).json()},
                                            {"booking": Booking.objects.get(id=booking6.id).json()},
                                        ]
                        }
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    @tag('locationschedule')
    def test_view_locationschedule_return_full_schedule(self):
        """ GIVEN 3 availabilities for 2021-01-04 at location 2, 1 booked; WHEN requesting schedule for 2021-01-04 at location 2; 1 booking and 2 availabilities should be returned """
        request = self.factory.get(reverse('policorp:locationschedule', kwargs={'locationid': 2, 'date': '20210104'}))
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        request.user = user
        location = Location.objects.get(pk=2)
        location.assign_supervisor(user)
        booker4 = aux.createUser('bar', 'bar@example.com', 'example')
        booking4 = Booking.objects.book(Availability.objects.get(pk=4), booker4)

        expected_data = {
                            'date': '2021-01-04',
                            'location': location.json(),
                            'schedule': [
                                            {"booking": Booking.objects.get(id=booking4.id).json()},
                                            {"availability": Availability.objects.get(pk=5).json()},
                                            {"availability": Availability.objects.get(pk=6).json()}
                                        ]
                        }

        response = locationschedule(request, 2, '20210104')
        logging.debug(str(response.content, encoding='utf8'))
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

if __name__ == "__main__":
    unittest.main()
