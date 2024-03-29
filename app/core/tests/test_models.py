"""
Tests for models
"""
from django.forms.fields import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="test@example.com", password="testP@55w0rd", **params):
    """Create and return a new User"""
    return get_user_model().objects.create_user(email, password, **params)


class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_with_email(self):
        """Test that user with email is created properly"""
        email = "normal_user@example.com"
        password = "iamPassw0rd"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new uerrs"""
        sample_email = [
            ["test1@Example.com", "test1@example.com"],
            ["Test2@example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, "iamPassw0rd")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            "testadmin@example.com",
            "testpasss",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating recipes"""
        user = get_user_model().objects.create_user(
            "testUser@example.com", "test pass word"
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe Name ",
            time_minutes=7,
            price=Decimal("7.99"),
            description="This is a sample recipe title",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful"""

        user = create_user()
        tag = models.Tags.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)
