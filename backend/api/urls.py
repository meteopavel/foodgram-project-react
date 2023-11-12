from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import RecipeViewSet

v1_router = DefaultRouter()

v1_router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(v1_router.urls)),
]