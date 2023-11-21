from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from api.views import (TokenJWTViewSet)

v1_router = DefaultRouter()

# v1_router.register('ingredients', IngredientViewSet, basename='ingredients')
# v1_router.register('recipes', RecipeViewSet, basename='recipes')
# v1_router.register('tags', TagViewSet, basename='tags')
# v1_router.register('users', UserListViewSet, basename='users')
# v1_router.register('users/me/', ProfileViewSet, basename='user-profile')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]





















"""
    path('auth/token/login/',
         TokenJWTViewSet.as_view({'post': 'create'}),
         name='get-jwt-token'),
    path('auth/token/logout/',
         TokenJWTViewSet.as_view({'post': 'destroy'}),
         name='destroy-jwt-token')
"""
