from django.test import TestCase, Client
from django.urls import reverse
import aux


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

if __name__ == "__main__":
    unittest.main()
