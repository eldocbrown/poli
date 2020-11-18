from django.test import TestCase, RequestFactory
import json
from policorp.models import Availability, Location, Task
from policorp.views import *
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_view_tasks_return_200(self):
        """ GIVEN ; WHEN GET /policorp/tasks ; THEN code 200 should be returned """
        task_name1 = "Device Installation"
        t1 = Task.objects.create_task(task_name1)
        j1 = {'id': 1, 'name': task_name1}
        task_name2 = "Repair"
        t2 = Task.objects.create_task(task_name2)
        j2 = {'id': 2, 'name': task_name2}

        # Create an instance of a GET request.
        request = self.factory.get(reverse('policorp:tasks'))
        response = tasks(request)
        self.assertEqual(response.status_code, 200)

    def test_view_tasks_post_not_allowed(self):
        """ GIVEN ; WHEN POST /policorp/tasks; THEN code 400 should be returned """
        # Create an instance of a POST request.
        request = self.factory.post('/policorp/tasks')
        response = tasks(request)
        self.assertEqual(response.status_code, 400)

    def test_view_tasks_return_2_tasks(self):
        """ GIVEN 2 tasks with name "Device Installation" and "Repair"; WHEN GET /policorp/tasks ; THEN 2 tasks should be returned in json format """
        task_name1 = "Device Installation"
        t1 = Task.objects.create_task(task_name1)
        j1 = {'id': 1, 'name': task_name1}
        task_name2 = "Repair"
        t2 = Task.objects.create_task(task_name2)
        j2 = {'id': 2, 'name': task_name2}
        expected_data = [j1, j2]

        # Create an instance of a GET request.
        request = self.factory.get('/policorp/tasks')
        response = tasks(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

if __name__ == "__main__":
    unittest.main()
