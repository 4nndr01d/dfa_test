import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    user_data = {
        "username": 'testuser',
        "password": '12345',
    }

    def setUp(self) -> None:
        self.user = User.objects.create_user(username=self.user_data['username'], password=self.user_data['password'])

    def test_user_registration(self):
        user_data = {
            "username": "testuser123",
            "email": "test@testuser.com",
            "password": "123123",
            "confirm_password": "123123"
        }
        response = self.client.post(reverse("profile-registration"), user_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue("username" in json.loads(response.content))
        self.assertEqual(user_data['username'], json.loads(response.content)['username'])

    def test_get_token(self):
        user_data = {
            "username": self.user_data['username'],
            "password": self.user_data['password'],
        }
        response = self.client.post(reverse("token_obtain"), user_data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("refresh" in json.loads(response.content))
        self.assertTrue("access" in json.loads(response.content))

    def test_refresh_token(self):
        user_data = {
            "username": self.user_data['username'],
            "password": self.user_data['password'],
        }
        get_token = self.client.post(reverse("token_obtain"), user_data)
        data = json.loads(get_token.content)
        refresh = self.client.post(reverse("token_refresh"), {'refresh': data['refresh']})
        self.assertEqual(200, refresh.status_code)
        self.assertTrue("refresh" in json.loads(refresh.content))
        self.assertTrue("access" in json.loads(refresh.content))
