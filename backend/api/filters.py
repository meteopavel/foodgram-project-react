from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    is_favorited = filters.BooleanFilter(method='_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def _is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return self.queryset.filter(favorites__user=self.request.user)
        return queryset

    def _in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return self.queryset.filter(shoppingcarts__user=self.request.user)
        return queryset
