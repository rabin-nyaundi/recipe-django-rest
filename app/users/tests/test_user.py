from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("users:create")
USER_TOKEN = reverse("users:token")
USER_PROFILE = reverse("users:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


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

    def create_user_token(self):
        """Test that the token is created for user"""
        payload = {"email": "test@user.com", "password": "testuserpass", "name": "Test user"}
        create_user(payload)

        res = self.client.post(USER_TOKEN, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def create_token_invalid_credentials(self):
        """Test token not created invalid credentials given"""
        create_user(email="test@user.com", password="testuserpass")
        payload = {"email": "test@user.com", "password": "wrong"}

        res = self.client.post(USER_TOKEN, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def create_token_no_user(self):
        """Test that no token is created if no user"""
        payload = {"email": "test@user.com", "password": "testuserpass", "name": "Test user"}

        res = self.client.post(USER_TOKEN, payload)
        self.assertNotIn("token", res.data)
        self.assertequal(res.status_code, status.HTTP_400_BAD_REQUEST)

    def create_token_missing_field(self):
        """Test to create token with missing user field"""
        payload = {"email": "test@user.com"}

        res = self.client.post(USER_TOKEN, payload)

        self.assertNotIn("token", res.data)
        self.assertequal(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_authenticated(self):
        """Test that user is authenticated"""
        res = self.client.get(USER_PROFILE)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(email="test@gmail.com", password="pass@word", name="Test user")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def retrieve_user_profile_success(self):
        """Test retrieving the user profile for logged in user"""
        res = self.client.get(USER_PROFILE)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})

    def test_post_profile_not_allowed(self):
        """Test that user is not allowed to make post request to profile url"""
        res = self.client.post(USER_PROFILE, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test update user profile"""
        payload = {"email": "test1@gmail.com", "name": "name", "password": "password4"}

        res = self.client.patch(USER_PROFILE, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.self.user.check_password(payload["password"]))
