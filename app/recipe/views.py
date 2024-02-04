"""
Views for recipe API endpoint
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from serializers import RecipeSerializer 


