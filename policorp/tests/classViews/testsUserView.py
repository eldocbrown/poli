from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from policorp.classViews.userView import UserView
from policorp.models import User
from policorp.tests import aux
import json

class TestUserView(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

    def test_userView_POST_return_405(self):
        """ GIVEN ; WHEN POST /policorp/user/foo ; THEN code 405 should be returned """
        username = 'foo'
        u1 = aux.createUser(username, 'foo@example.com', 'example')
        request = self.factory.post(reverse('policorp:user', kwargs={'username': username}))
        force_authenticate(request, user=u1)
        response = UserView.as_view()(request, username)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_userView_GET_authenticated_foo_return_200(self):
        """ GIVEN ; WHEN GET /policorp/user/foo ; THEN code 200 should be returned """
        username = 'foo'
        u1 = aux.createUser(username, 'foo@example.com', 'example')
        request = self.factory.get(reverse('policorp:user', kwargs={'username': username}))
        force_authenticate(request, user=u1)
        response = UserView.as_view()(request, username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_userView_GET_not_authenticated_foo_return_403(self):
        """ GIVEN ; WHEN GET /policorp/user/foo ; THEN code 200 should be returned """
        username = 'foo'
        u1 = aux.createUser(username, 'foo@example.com', 'example')
        request = self.factory.get(reverse('policorp:user', kwargs={'username': username}))
        response = UserView.as_view()(request, username)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_userView_GET_another_user_cannot_see_my_user_details(self):
        """ GIVEN ; WHEN GET /policorp/user/foo ; THEN code 403 should be returned """
        username = 'foo'
        u1 = aux.createUser(username, 'foo@example.com', 'example')
        u2 = aux.createUser('bar', 'bar@example.com', 'example')
        request = self.factory.get(reverse('policorp:user', kwargs={'username': username}))
        force_authenticate(request, user=u2)
        response = UserView.as_view()(request, username)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_userView_GET_supervisor_user_can_see_my_user_details(self):
        """ GIVEN ; WHEN authenticated supervisor GET /policorp/user/foo ; THEN code 200 should be returned """
        username = 'foo'
        u1 = aux.createUser(username, 'foo@example.com', 'example')
        request = self.factory.get(reverse('policorp:user', kwargs={'username': username}))
        supervisor = User.objects.create_supervisor('bar', 'bar@example.com', 'example')
        force_authenticate(request, user=supervisor)
        response = UserView.as_view()(request, username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_userView_GET_authenticated_foo_returns_200_and_user_data(self):
        """ GIVEN ; WHEN GET /policorp/user/foo ; THEN code 200 should be returned """
        username = "foo"
        email = "foo@example.com"
        password = "example"
        first_name = "Nombre"
        last_name = "Apellido"

        u1 = aux.createUser(username, email, password, first_name, last_name)
        request = self.factory.get(reverse('policorp:user', kwargs={'username': username}))
        force_authenticate(request, user=u1)
        response = UserView.as_view()(request, username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_json = {
            "username":  username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }

        self.assertJSONEqual(json.dumps(response.data), expected_json)
