from django.contrib.auth import get_user_model
#from djoser.serializers import UserCreateSerializer


User = get_user_model()



#class CustomUserSerializer(UserCreateSerializer):
#    class Meta:
#        model = User
#        fields = ('email', 'username', 'first_name', 'last_name', 'password')































"""
class TokenSerializer(TokenSerializer):
    email = serializers.CharField()
    password = serializers.CharField()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
"""

"""
class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserListSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
"""


"""
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
"""

"""
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag
from djoser.serializers import TokenSerializer
"""
