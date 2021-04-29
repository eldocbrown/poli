from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from datetime import datetime, timezone, timedelta
import json
from policorp.tests import aux
from policorp.models import Availability, Location, Task, User, Booking
from policorp.classViews.bookOnTheFlyView import BookOnTheFlyView

import sys

class TestBookingOnTheFlyView(TestCase):

    fixtures = ['testsdata.json']

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

    def test_bookOnTheFlyView_location_supervisor_creates_new_availability_and_booking(self):

        u1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')

        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        cancelled = False
        note = 'A note for my schedule'

        location = Location.objects.get(pk=locationid)
        location.assign_supervisor(u1)

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

        request = self.factory.post(reverse('policorp:bookonthefly'), json.dumps(booking, cls=aux.DateTimeEncoder), content_type='application/json')

        force_authenticate(request, user=u1)
        response = BookOnTheFlyView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        booking = Booking.objects.get(user=u1)
        self.assertIsNotNone(booking)

    def test_bookOnTheFlyView_only_authenticated_users_can_post(self):

        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        note = 'A note for my schedule'

        booking = {
            'availability': {
                'when': now.isoformat(),
                'where': locationid,
                'what': taskid
            },
            'note': note,
            'user': 'zoe'
        }

        request = self.factory.post(reverse('policorp:bookonthefly'), json.dumps(booking, cls=aux.DateTimeEncoder), content_type='application/json')

        response = BookOnTheFlyView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bookOnTheFlyView_only_authenticated_supervisors_users_can_post(self):

        u1 = aux.createUser('foo', 'foo@example.com', 'example')

        now = datetime.now(tz=timezone.utc)
        locationid = 1
        taskid = 1
        note = 'A note for my schedule'

        booking = {
            'availability': {
                'when': now.isoformat(),
                'where': locationid,
                'what': taskid
            },
            'note': note,
            'user': u1.username
        }

        request = self.factory.post(reverse('policorp:bookonthefly'), json.dumps(booking, cls=aux.DateTimeEncoder), content_type='application/json')

        force_authenticate(request, user=u1)
        response = BookOnTheFlyView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bookOnTheFlyView_only_an_authenticated_location_supervisor_at_that_location_can_post(self):

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

        request = self.factory.post(reverse('policorp:bookonthefly'), json.dumps(booking, cls=aux.DateTimeEncoder), content_type='application/json')

        force_authenticate(request, user=u1)
        response = BookOnTheFlyView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
