from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("users:create")


def create_user(**params):
    return get_user_model.objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user with valid payload successful"""
        payload = {"email": "test@user.com", "password": "testuserpass", "name": "Test user"}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_password_too_short(self):
        """Test check user password is more 8 characters long"""
        payload = {"email": "test@user.com", "password": "test", "name": "Test user"}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload.get("email")).exists()

        self.assertFalse(user_exists)

    def user_exists(self):
        """Tests creating a user already exists fails"""
        payload = {"email": "test@user.com", "password": "testuserpass", "name": "Test user"}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
