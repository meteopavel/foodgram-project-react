from django.contrib.auth import authenticate, get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ReadOnlyModelViewSet,
                                     ModelViewSet)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import serializers

from api.serializers import (IngredientSerializer, RecipeSerializer,
                             TagSerializer, TokenSerializer, UserSerializer)
from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination


class ProfileViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    #def get_queryset(self, request):
    #    return get_object_or_404(request.user)


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
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination


class TokenJWTViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_from_email = User.objects.get(
                email=serializer.validated_data['email']
            )
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username/password!")

        user = authenticate(
            username=user_from_email.username,
            password=serializer.validated_data['password']
        )
        if user is None:
            raise serializers.ValidationError("Invalid username/password!")
        if user is not None:
            token = AccessToken.for_user(user)
            return Response(
                {'auth_token': str(token)},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)
