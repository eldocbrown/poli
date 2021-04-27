from django.test import TestCase
import json
from policorp.serializers import UserSerializer
from policorp.tests import aux

class TestUserSerializer(TestCase):

    def test_userSerializer_full(self):
        username = "foo"
        email = "foo@example.com"
        password = "example"
        first_name = "Nombre"
        last_name = "Apellido"

        user = aux.createUser(username, email, password, first_name, last_name)
        serializer = UserSerializer(instance=user)
        data = serializer.data

        expected_json = {
            "username":  username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }

        self.assertJSONEqual(json.dumps(data), expected_json)

    def test_userSerializer_no_first_name(self):
        username = "foo"
        email = "foo@example.com"
        password = "example"
        first_name = None
        last_name = "Apellido"

        user = aux.createUser(username, email, password, first_name, last_name)
        serializer = UserSerializer(instance=user)
        data = serializer.data

        expected_json = {
            "username":  username,
            "email": email,
            "first_name": '',
            "last_name": last_name
        }

        self.assertJSONEqual(json.dumps(data), expected_json)

    def test_userSerializer_no_last_name(self):
        username = "foo"
        email = "foo@example.com"
        password = "example"
        first_name = "Nombre"

        user = aux.createUser(username, email, password, first_name)
        serializer = UserSerializer(instance=user)
        data = serializer.data

        expected_json = {
            "username":  username,
            "email": email,
            "first_name": first_name,
            "last_name": ''
        }

        self.assertJSONEqual(json.dumps(data), expected_json)
