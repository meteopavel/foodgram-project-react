from recipes.models import IngredientRecipe


def create_ingredients(recipe, ingredients):
    for ingredient in ingredients:
        IngredientRecipe.objects.create(
            recipe=recipe,
            ingredient=(ingredient.get('ingredient'))['id'],
            amount=ingredient.get('amount')
        )
