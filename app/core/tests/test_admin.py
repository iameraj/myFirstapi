"""
Test for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTest(TestCase):
    """Test for Django Amin."""

    def setUp(self):
        """Create user and Client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="konoAdminDA",
            email="admin_user@example.com",
            password="iamPassw0rd",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="normal_user@example.com",
            password="iamPassw0rd",
            username="normal_test_user",
        )

    def test_users_list(self):
        """Test that users are listed on page"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
