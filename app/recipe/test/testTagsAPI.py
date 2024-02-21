"""
Tests for Tags API
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tags
from recipe.serializers import TagsSerializer

TAGS_URL = reverse("recipe:tag-list")


def create_user(email="test@example.com", password="testP@55w0rd", **params):
    """Create and return a new User"""
    return get_user_model().objects.create_user(email, password, **params)


class PublicTagsApiTests(TestCase):
    """Test API endpoint for unauthenticated requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required for retrieving tags."""

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test API endpoint for authenticated requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Tests retrieving list of tags."""

        Tags.objects.create(user=self.user, name="Vegan")
        Tags.objects.create(user=self.user, name="Sweets")

        res = self.client.get(TAGS_URL)

        tags = Tags.objects.all().order_by("-name")
        serializer = TagsSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
