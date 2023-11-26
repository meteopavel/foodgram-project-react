import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer, ImageField

from recipes.models import Tag, Ingredient, Recipe, TagRecipe

User = get_user_model()


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    # С этим пока всё непонятно. Нужно доразобраться
    # https://practicum.yandex.ru/learn/python-developer-plus/courses/ff822384-ebee-4c94-b637-107f18eb1678/sprints/134994/topics/ab7ab7e6-9e2e-400c-9868-189eb5f5fe7e/lessons/e5ee1212-c9e0-49a6-bc19-b95791a38f2a/
    def create(self, validated_data):
        tags = validated_data.pop('tags_id')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            current_tag = Tag.objects.get_or_create(tag)
            TagRecipe.objects.create(tag=current_tag, recipe=recipe)
        return recipe


class UserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
