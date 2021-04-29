from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from datetime import datetime, timezone, timedelta
from policorp.classViews.availabilityView import AvailabilityView
from policorp.models import Availability, Location, Task, User, Booking

class TestAvailabilityView(TestCase):

    fixtures = ['testsdata.json']

    task1 = {'id': 1, 'name': 'Device Installation', 'duration': 120}
    task2 = {'id': 2, 'name': 'Repair', 'duration': 60}

    maxDiff = None

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

    def test_availabilityView_GET_return_405(self):
        """ GIVEN ; WHEN GET /policorp/availability/1 ; THEN code 405 should be returned """
        # Create an instance of a GET request.
        availabilityid = 1
        request = self.factory.get(reverse('policorp:availability', kwargs={'availabilityid': availabilityid}))
        response = AvailabilityView.as_view()(request, availabilityid)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_availabilityView_unauthenticated_delete_request_forbidden(self):
        """ GIVEN ; WHEN DELETE /policorp/availability/1 unauthenticated ; THEN code 403 should be returned """
        availabilityid = 1
        request = self.factory.delete(reverse('policorp:availability', kwargs={'availabilityid': availabilityid}))
        response = AvailabilityView.as_view()(request, availabilityid)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_availabilityView_supervisor_cant_delete_availability(self):
        """ GIVEN an availability at a not supervised location; WHEN DELETE /policorp/availability/1 ; THEN code 403 should be returned """

        now = datetime.now(timezone.utc)
        l1 = Location.objects.get(pk=1)
        task_name = "Device Installation for Trucks"
        t1 = Task.objects.create_task(task_name, 120)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 60), l1, t1)
        u1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')

        availabilityid = a1.id
        request = self.factory.delete(reverse('policorp:availability', kwargs={'availabilityid': availabilityid}))
        force_authenticate(request, user=u1)
        response = AvailabilityView.as_view()(request, availabilityid)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_availabilityView_supervisor_deletes_availability(self):
        """ GIVEN an availability in a supervised location; WHEN DELETE /policorp/availability/1 ; THEN code 204 should be returned """

        now = datetime.now(timezone.utc)
        l1 = Location.objects.get(pk=1)
        task_name = "Device Installation for Trucks"
        t1 = Task.objects.create_task(task_name, 120)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 60), l1, t1)
        u1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        l1.assign_supervisor(u1)

        availabilityid = a1.id
        request = self.factory.delete(reverse('policorp:availability', kwargs={'availabilityid': availabilityid}))
        force_authenticate(request, user=u1)
        response = AvailabilityView.as_view()(request, availabilityid)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_availabilityView_cant_delete_if_booked(self):
        """ GIVEN a booked availability; WHEN DELETE /policorp/availability/1 ; THEN code 409 should be returned """

        now = datetime.now(timezone.utc)
        l1 = Location.objects.get(pk=1)
        task_name = "Device Installation for Trucks"
        t1 = Task.objects.create_task(task_name, 120)
        a1 = Availability.objects.create_availability(now + timedelta(minutes = 60), l1, t1)
        u1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        l1.assign_supervisor(u1)
        booking = Booking.objects.book(a1, u1)

        availabilityid = a1.id
        request = self.factory.delete(reverse('policorp:availability', kwargs={'availabilityid': availabilityid}))
        force_authenticate(request, user=u1)
        response = AvailabilityView.as_view()(request, availabilityid)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        response.render()
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"detail": "Availability is already booked."})
