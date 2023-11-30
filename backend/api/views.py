from django.db.models import Sum
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (TagSerializer,
                             IngredientSerializer,
                             RecipeGetSerializer,
                             RecipePostSerializer,
                             SubscriptionsListSerializer,
                             GetRemoveSubscriptionSerializer,
                             ShoppingCartSerializer,
                             FavoriteSerializer)
from api.utils import (draw_pdf_report,
                       _create_related_object,
                       _delete_related_object)
from recipes.models import (Tag, Ingredient, Recipe,
                            ShoppingCart, IngredientRecipe, Favorite)
from users.models import Subscription

User = get_user_model()


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipePostSerializer
        return RecipeGetSerializer

    @action(detail=True,
            permission_classes=(IsAuthenticated,), methods=('post',))
    def shopping_cart(self, request, pk):
        """Добавление и удаление рецептов из списка покупок."""
        return _create_related_object(pk, request, ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        return _delete_related_object(pk, request, ShoppingCart)

    @action(methods=('get',), detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Скачивание списка покупок."""
        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__shoppingcarts__user=request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit'
            ).annotate(
                ingredient_amount=Sum(
                    'amount'
                )
            ).order_by(
                'ingredient__name'
            )
        )
        return draw_pdf_report(ingredients)

    @action(detail=True,
            permission_classes=(IsAuthenticated,), methods=('post',))
    def favorite(self, request, pk):
        """Добавление и удаление рецептов из избранного."""
        return _create_related_object(pk, request, FavoriteSerializer)

    @favorite.mapping.delete
    def unmake_recipe_favorite(self, request, pk):
        return _delete_related_object(pk, request, Favorite)


class UserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination

    @action(detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request, format=None):
        return Response(self.serializer_class(request.user).data)

    @action(detail=False,
            permission_classes=(IsAuthenticated,),
            serializer_class=SubscriptionsListSerializer)
    def subscriptions(self, request):
        queryset = self.filter_queryset(
            User.objects.filter(following__user=self.request.user)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, permission_classes=(IsAuthenticated,),
            methods=('post',))
    def subscribe(self, request, id):
        """Action для работы с подписками пользователей."""
        serializer = GetRemoveSubscriptionSerializer(
            data={
                'user': request.user.id,
                'author': id},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
        if not Subscription.objects.filter(
                user=request.user, author_id=id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.filter(
            user=request.user, author=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
