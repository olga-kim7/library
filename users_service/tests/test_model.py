from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from users_service.models import User

USER_URL = reverse("users_service:register")


class TestUserModel(TestCase):

    def test_create_user_with_username(self):
        user = {
            'username': 'test_test',
            "password": "Test12345",
        }
        response = self.client.post(USER_URL, user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_email(self):
        user = {
            "email": "test@gmail.com",
            "password": "Test12345",
        }
        response = self.client.post(USER_URL, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
