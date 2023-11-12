from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.serializers import RecipeSerializer
from recipes.models import Recipe



class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)
