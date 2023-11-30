from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class UserRecipeBaseModel(models.Model):
    """Базовая модель для списков покупок и избранных рецептов."""

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        default_related_name = '%(class)ss'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='%(app_label)s_%(class)s relation already exists.',
            )
        ]
        abstract = True


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=32,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        verbose_name='Slug тега'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Единицы измерения'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    is_favorited = models.BooleanField(
        'Избранное',
        default=False,
        help_text='Поставьте галочку, чтобы добавить в избранное.'
    )
    is_in_shopping_cart = models.BooleanField(
        'В списке покупок',
        default=False,
        help_text='Поставьте галочку, чтобы добавить в список покупок.'
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name='Изображение блюда'
    )
    text = models.TextField(
        verbose_name='Текст рецепта'
    )
    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(1, 'Время не может быть ниже 1'),),
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class Favorite(UserRecipeBaseModel):
    class Meta(UserRecipeBaseModel.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избранное.'


class ShoppingCart(UserRecipeBaseModel):
    class Meta(UserRecipeBaseModel.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.user.username} добавил'
                f' {self.recipe.name} в список покупок.')


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField(
        validators=(
            MinValueValidator(1, 'Количество не может быть ниже 1'),)
    )

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'
