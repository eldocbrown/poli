from django.test import TestCase, RequestFactory, tag
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.core.serializers.json import DjangoJSONEncoder
import json
from policorp.models import Availability, Location, Task, Booking
from policorp.views import *
from policorp.tests import aux
from datetime import datetime, timezone


class TestCreateAvailabilityViews(TestCase):

    fixtures = ['testsdata.json']

    task1 = {'id': 1, 'name': 'Device Installation', 'duration': 120}
    task2 = {'id': 2, 'name': 'Repair', 'duration': 60}

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    @tag('createavailabilitysingle')
    def test_view_createavailabilitysingle_only_post_allowed(self):
        """ GIVEN ; WHEN GET /policorp/createavailabilitysingle; THEN code 400 should be returned """
        request = self.factory.get(reverse('policorp:createavailabilitysingle'))
        response = createavailabilitysingle(request)
        self.assertEqual(response.status_code, 400)

    @tag('createavailabilitysingle')
    def test_view_createavailabilitysingle_only_logged_in_requests_allowed(self):
        """ GIVEN ; WHEN POST /policorp/createavailabilitysingle logged out; THEN code 401 (unauthorized) should be returned """
        request = self.factory.post(reverse('policorp:createavailabilitysingle'))
        request.user = AnonymousUser()
        response = createavailabilitysingle(request)
        self.assertEqual(response.status_code, 401)

    @tag('createavailabilitysingle')
    def test_view_createavailabilitysingle_only_logged_in_supervisor_requests_allowed(self):
        """ GIVEN ; WHEN POST /policorp/createavailabilitysingle logged in with non supervisor user; THEN code 401 (unauthorized) should be returned """
        request = self.factory.post(reverse('policorp:createavailabilitysingle'))
        request.user = aux.createUser('foo', 'foo@example.com', 'example')
        response = createavailabilitysingle(request)
        self.assertEqual(response.status_code, 401)

    @tag('createavailabilitysingle')
    def test_view_createavailabilitysingle_returns_201_and_created_availability(self):
        """ GIVEN ; WHEN POST /policorp/createavailabilitysingle with json content (location 1; task 1; (today + 1) at 14:00 utc time); THEN code 201 should be returned """
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        location = Location.objects.get(pk=1).assign_supervisor(user)
        now = datetime.now(timezone.utc)
        body = {
            "locationid": 1,
            "taskid": 1,
            "when": datetime(now.year, now.month, now.day + 1, 14, 0, 0, 0, tzinfo=timezone.utc)
        }
        request = self.factory.post(    reverse('policorp:createavailabilitysingle'),
                                        data=json.dumps(body, cls=aux.DateTimeEncoder),
                                        content_type='application/json')
        request.user = user
        response = createavailabilitysingle(request)
        self.assertEqual(response.status_code, 201)
        expected_json = Availability.objects.all().order_by("-id")[0].json()
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('createavailabilitysingle')
    def test_view_createavailabilitysingle_returns_401_when_not_supervising_location(self):
        """ GIVEN ; WHEN POST /policorp/createavailabilitysingle with json content (location 1; task 1; (today + 1) at 14:00 utc time), not supervising location 1; THEN code 401 should be returned """
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        now = datetime.now(timezone.utc)
        body = {
            "locationid": 1,
            "taskid": 1,
            "when": datetime(now.year, now.month, now.day + 1, 14, 0, 0, 0, tzinfo=timezone.utc)
        }
        request = self.factory.post(    reverse('policorp:createavailabilitysingle'),
                                        data=json.dumps(body, cls=aux.DateTimeEncoder),
                                        content_type='application/json')
        request.user = user
        response = createavailabilitysingle(request)
        self.assertEqual(response.status_code, 401)

    @tag('createavailabilities')
    def test_view_createavailabilities_only_post_allowed(self):
        """ GIVEN ; WHEN GET /policorp/createavailabilities; THEN code 400 should be returned """
        request = self.factory.get(reverse('policorp:createavailabilities'))
        response = createavailabilities(request)
        self.assertEqual(response.status_code, 400)

    @tag('createavailabilities')
    def test_view_createavailabilities_only_logged_in_requests_allowed(self):
        """ GIVEN ; WHEN POST /policorp/createavailabilities logged out; THEN code 401 (unauthorized) should be returned """
        request = self.factory.post(reverse('policorp:createavailabilities'))
        request.user = AnonymousUser()
        response = createavailabilities(request)
        self.assertEqual(response.status_code, 401)

    @tag('createavailabilities')
    def test_view_createavailabilities_only_logged_in_supervisor_requests_allowed(self):
        """ GIVEN ; WHEN POST /policorp/createavailabilities logged in with non supervisor user; THEN code 401 (unauthorized) should be returned """
        request = self.factory.post(reverse('policorp:createavailabilities'))
        request.user = aux.createUser('foo', 'foo@example.com', 'example')
        response = createavailabilities(request)
        self.assertEqual(response.status_code, 401)

    @tag('createavailabilities')
    def test_view_createavailabilities_returns_201_and_created_2_availabilities(self):
        """ GIVEN ; WHEN POST /policorp/createavailabilities with json content (location 1; task 1; (today + 1) at 14:00 utc time) + (location 1; task 1; (today + 1) at 16:00 utc time); THEN code 201 should be returned """
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        location = Location.objects.get(pk=1).assign_supervisor(user)
        now = datetime.now(timezone.utc)
        body = [
        {
            "locationid": 1,
            "taskid": 1,
            "when": datetime(now.year, now.month, now.day + 1, 14, 0, 0, 0, tzinfo=timezone.utc)
        },
        {
            "locationid": 1,
            "taskid": 1,
            "when": datetime(now.year, now.month, now.day + 1, 16, 0, 0, 0, tzinfo=timezone.utc)
        }
        ]
        request = self.factory.post(    reverse('policorp:createavailabilitysingle'),
                                        data=json.dumps(body, cls=aux.DateTimeEncoder),
                                        content_type='application/json')
        request.user = user
        response = createavailabilities(request)
        self.assertEqual(response.status_code, 201)
        expected_json = [
            Availability.objects.all().order_by("-id")[1].json(),
            Availability.objects.all().order_by("-id")[0].json()
        ]
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    @tag('createavailabilities')
    def test_view_createavailabilities_returns_401_when_not_supervising_location(self):
        """ GIVEN ; WHEN POST /policorp/createavailabilities with json content (location 1; task 1; (today + 1) at 14:00 utc time) + (location 2; task 1; (today + 1) at 16:00 utc time), not supervising location 2; THEN code 401 should be returned """
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        location = Location.objects.get(pk=1).assign_supervisor(user)
        now = datetime.now(timezone.utc)
        body = [
        {
            "locationid": 1,
            "taskid": 1,
            "when": datetime(now.year, now.month, now.day + 1, 14, 0, 0, 0, tzinfo=timezone.utc)
        },
        {
            "locationid": 2,
            "taskid": 1,
            "when": datetime(now.year, now.month, now.day + 1, 16, 0, 0, 0, tzinfo=timezone.utc)
        }
        ]
        request = self.factory.post(    reverse('policorp:createavailabilitysingle'),
                                        data=json.dumps(body, cls=aux.DateTimeEncoder),
                                        content_type='application/json')
        request.user = user
        response = createavailabilities(request)
        self.assertEqual(response.status_code, 201)
        expected_json = [
            Availability.objects.all().order_by("-id")[0].json(),
            {
                "locationid": 2,
                "taskid": 1,
                "when": datetime(now.year, now.month, now.day + 1, 16, 0, 0, 0, tzinfo=timezone.utc),
                "error": "Unauthorized"
            }
        ]
        self.assertJSONEqual(str(response.content, encoding='utf8'), json.dumps(expected_json, cls=aux.DateTimeEncoder))

if __name__ == "__main__":
    unittest.main()
