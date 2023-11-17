from django.contrib import admin

from recipes.models import Ingredient, TagRecipe, Recipe


class TagRecipeInline(admin.StackedInline):
    model = TagRecipe
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        TagRecipeInline,
    )
    list_display = (
        'id', 'author', 'is_favorited',
        'is_in_shopping_cart', 'name', 'cooking_time'
    )
    list_editable = (
        'author', 'is_favorited',
        'is_in_shopping_cart', 'name', 'cooking_time'
    )
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(Ingredient)
admin.site.register(TagRecipe)
admin.site.register(Recipe, RecipeAdmin)
