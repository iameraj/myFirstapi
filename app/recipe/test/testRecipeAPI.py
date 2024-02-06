"""
Tests for Recipe APi
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe 
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        "title": "sample recipe title",
        "time_minutes": 23,
        "price": Decimal("4.64"),
        "description": "This is a sample recipe description",
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)

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
        self.user = create_user(email="test@example.com", password= "testpassword")
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        """Tests retrieving recipes"""

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")

        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(serializer.data, res.data)

    def test_get_recipe_detail(self):
        """Test getting recipe details"""

        recipe = create_recipe(user=self.user)
        url = detail_url(recipe_id=recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating recipe"""

        payload = {
            "title": "Sample",
            "price": Decimal("4.34"),
            "time_minutes": 15,
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        recipe = Recipe.objects.get(id=res.data["id"])

        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)
