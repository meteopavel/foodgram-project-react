import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        HiddenField, ModelSerializer,
                                        ImageField, PrimaryKeyRelatedField,
                                        SerializerMethodField)

from recipes.models import Tag, Ingredient, Recipe, IngredientRecipe
User = get_user_model()


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(source='ingredient.id',
                                queryset=Ingredient.objects.all())
    measurement_unit = CharField(source='ingredient.measurement_unit',
                                 read_only=True)
    name = CharField(source='ingredient.name', read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


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


class RecipeGetSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe_id=obj.id)
        return IngredientRecipeSerializer(ingredients, many=True).data


class RecipePostSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(many=True,
                                  queryset=Tag.objects.all())
    author = HiddenField(default=CurrentUserDefault())
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')
        read_only_fields = ('author',)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=(ingredient.get('ingredient'))['id'],
                amount=ingredient.get('amount')
            )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients')
        IngredientRecipe.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=instance,
                ingredient=(ingredient.get('ingredient'))['id'],
                amount=ingredient.get('amount')
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeGetSerializer(instance,
                                   context=self.context).data


class UserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
