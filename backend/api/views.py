from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (TagSerializer, UserSerializer,
                             IngredientSerializer, RecipeSerializer)
from recipes.models import Tag, Ingredient, Recipe

User = get_user_model()


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination


class UserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = UserSerializer

    @action(detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request, format=None):
        return Response(self.serializer_class(request.user).data)


"""
from django.contrib.auth import authenticate, get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ReadOnlyModelViewSet,
                                     ModelViewSet)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import serializers

from api.serializers import (TokenSerializer)
from recipes.models import Ingredient, Recipe, Tag
"""
