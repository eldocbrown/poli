from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timezone
import json
from policorp.tests import aux
from policorp.models import Availability, Booking, User, Location

class TestClient(TestCase):

    fixtures = ['testsdata.json']

    def test_tasks_view_return_200(self):
        """*** Tasks view get request needs to be with response 200 ***"""
        c = Client()
        response = c.get(reverse('policorp:tasks'))
        self.assertEqual(response.status_code, 200)

    def test_availabilities_view_return_200(self):
        """*** Availabilities view get request needs to be with response 200 ***"""
        c = Client()
        response = c.get(reverse('policorp:availabilities', kwargs={'taskid': 1}))
        self.assertEqual(response.status_code, 200)

    def test_dailyavailabilities_view_return_200(self):
        """*** Daily Availabilities view get request needs to be with response 200 ***"""
        c = Client()
        datestr = datetime.now(timezone.utc).date().isoformat().replace('-','')
        response = c.get(reverse('policorp:dailyavailabilities', kwargs={'taskid': 1, 'date': datestr}))
        self.assertEqual(response.status_code, 200)

    def test_book_view_return_201(self):
        """*** Booking an availability with a post request should return 201 ****"""
        c = Client()
        u = aux.createUser('foo', 'foo@example.com', 'example')
        c.login(username='foo', password='example')
        response = c.post(reverse('policorp:book', kwargs={'availabilityid': 1}))
        self.assertEqual(response.status_code, 201)

    def test_myschedule_view_return_200(self):
        """*** My Schedule view get request needs to be with response 200, logged in ***"""
        c = Client()
        u = aux.createUser('foo', 'foo@example.com', 'example')
        c.login(username='foo', password='example')
        response = c.get(reverse('policorp:myschedule'))
        self.assertEqual(response.status_code, 200)

    def test_cancelbooking_view_return_201(self):
        """*** Cancelling a booking with a post request should return 201 ****"""
        user1 = aux.createUser('foo', 'foo@example.com', 'example')
        availability1 = Availability.objects.get(pk=1)
        b1 = Booking.objects.book(availability1, user1)
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(reverse('policorp:cancelbooking', kwargs={'bookingid': b1.id}))
        self.assertEqual(response.status_code, 201)

    def test_mysupervisedlocations_view_return_200(self):
        """*** My supervised locations get request needs to be with response 200 ***"""
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        Location.objects.get(pk=1).assign_supervisor(user)
        c = Client()
        c.login(username='foo', password='example')
        response = c.get(reverse('policorp:mysupervisedlocations'))
        self.assertEqual(response.status_code, 200)

    def test_locationschedule_view_return_200(self):
        """*** Location schedule get request needs to be with response 200 ***"""
        user = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        Location.objects.get(pk=1).assign_supervisor(user)
        c = Client()
        c.login(username='foo', password='example')
        response = c.get(reverse('policorp:locationschedule', kwargs={'locationid': 1, 'date': '20210102'}))
        self.assertEqual(response.status_code, 200)

    def test_createavailabilities_view_return_201(self):
        """*** Creating an availability with a post request should return 201 ****"""
        user1 = User.objects.create_supervisor('foo', 'foo@example.com', 'example')
        Location.objects.get(pk=1).assign_supervisor(user1)
        c = Client()
        c.login(username='foo', password='example')
        body = [{
            "locationid": 1,
            "taskid": 1,
            "when": datetime.now(tz=timezone.utc)
        }]
        response = c.post(  reverse('policorp:createavailabilities'),
                            data=json.dumps(body, cls=aux.DateTimeEncoder),
                            content_type='application/json')
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()
