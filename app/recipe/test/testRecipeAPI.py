"""
Tests for Recipe APi
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.serializers import serializers
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse("recipe:recipe-list")


def create_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        "title": "sample recipe title",
        "time_minutes": 23,
        "price": Decimal("4.64"),
        "description": "This is a sample recipe description",
        "link": "https://example.com",
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """
    Tests unauthenticated recipe endpoints
    """

    def setUp(self):
        self.client = APIClient()

    def testAuthRequired(self):
        """Test that auth is required for recipe"""

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """
    Tests Authenticated recipe endpoints
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com", 
            "test!password"
        )
        self.client.force_authenticate()

    def test_retrieve_recipes(self):
        """Tests retrieving recipes"""

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")

        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(serializer.data, res.data)

