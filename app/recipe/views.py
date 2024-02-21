"""
Views for recipe API endpoints
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tags
from recipe.serializers import (
    RecipeDetailSerializer,
    RecipeSerializer,
    TagsSerializer,
)


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

        if self.action == "list":
            return RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Method for creating Recipes"""
        serializer.save(user=self.request.user)


class TagsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Views to manage Tags View"""

    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve Tags for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-name")
