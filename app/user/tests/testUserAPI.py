"""
Tests for the User API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    """Create and return a new User"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public methods of user"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test for creating a user"""
        payload = {
            "email": "exampleUser01@example.com",
            "password": "testPass01",
            "name": "name01",
        }
        res = self.client.post(CREATE_USER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload["email"])
        self.assertEqual(user.name, payload["name"])

    def test_email_already_exists(self):
        """Test if a user cannnot create email that already exists"""

        payload = {
            "email": "exampleUser01@example.com",
            "password": "testPass01",
            "name": "name01",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_too_short(self):
        """Test if create_user does not work with short passwords"""

        payload = {
            "email": "exampleUser01@example.com",
            "password": "s01",
            "name": "name01",
        }
        res = self.client.post(CREATE_USER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )
        self.assertFalse(user_exists)

    def test_create_token_for_User(self):
        """Testing generation of tokens for valid credentials"""
        payload = {
            "email": "exampleUser02@example.com",
            "password": "testPass02",
            "name": "name02",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload, format="json")

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_bad_req(self):
        """Testing failing of token generation with invalid token"""

        user_details = {
            "name": "Test2Name",
            "email": "Tst2@example.com",
            "password": "testPassW",
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": "IamAIncorrectPassword",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_No_password(self):
        """Testing if token generation fails with no password"""

        payload = {"email": "Tst2@example", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
