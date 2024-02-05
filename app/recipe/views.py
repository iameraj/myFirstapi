"""
Views for recipe API endpoints
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Views to manage Recipe API endpoints"""

    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipe for authenticated user"""

        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request"""

        if self.action == 'list':
            return RecipeSerializer

        return self.serializer_class
