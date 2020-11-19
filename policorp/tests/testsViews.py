from django.test import TestCase, RequestFactory, tag
from django.urls import reverse
import json
import sys
from policorp.models import Availability, Location, Task
from policorp.views import *

class TestViews(TestCase):

    fixtures = ['testsdata.json']

    task1 = {'id': 1, 'name': 'Device Installation'}
    task2 = {'id': 2, 'name': 'Repair'}

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    @tag('tasks_view')
    def test_view_tasks_return_200(self):
        """ GIVEN ; WHEN GET /policorp/tasks ; THEN code 200 should be returned """
        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:tasks'))
        response = tasks(request)
        self.assertEqual(response.status_code, 200)

    @tag('tasks_view')
    def test_view_tasks_post_not_allowed(self):
        """ GIVEN ; WHEN POST /policorp/tasks; THEN code 400 should be returned """
        # Create an instance of a POST request.
        request = self.factory.post(reverse('policorp:tasks'))
        response = tasks(request)
        self.assertEqual(response.status_code, 400)

    @tag('tasks_view')
    def test_view_tasks_return_2_tasks(self):
        """ GIVEN 2 tasks with name "Device Installation" and "Repair"; WHEN GET /policorp/tasks ; THEN 2 tasks should be returned in json format """
        expected_data = [self.task1, self.task2]

        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:tasks'))
        response = tasks(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    @tag('availabilities_view')
    def test_view_availabilities_return_200(self):
        """ GIVEN ; WHEN GET /policorp/availabilities/1 ; THEN code 200 is returned """
        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:availabilities', kwargs={'taskid': 1}))
        response = availabilities(request, 1)
        self.assertEqual(response.status_code, 200)

    @tag('availabilities_view')
    def test_view_availabilities_return_1_availability(self):
        """ GIVEN ; WHEN GET /policorp/availabilities/1 ; THEN availabiliy 1 json is returned """
        expected_data = [Availability.objects.get(pk=2).json()]

        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:availabilities', kwargs={'taskid': 1}))
        response = availabilities(request, 1)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    @tag('availabilities_view')
    def test_view_tasks_post_not_allowed(self):
        """ GIVEN ; WHEN POST /policorp/availabilities/1; THEN code 400 is returned """
        # Create an instance of a POST request.
        request = self.factory.post(reverse('policorp:availabilities', kwargs={'taskid': 1}))
        response = availabilities(request, 1)
        self.assertEqual(response.status_code, 400)

    @tag('book_view')
    def test_view_book(self):
        """ GIVEN ; WHEN POST /policorp/availabilities/1 ; THEN code 201 is returned """
        request = self.factory.post(reverse('policorp:book', kwargs={'availabilityid': 1}))
        response = book(request, 1)
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
