from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView, status, Http404
from .models import RecipeIngredients

from fgapp.permissions import AuthorOrReadOnly, RecipeAuthor, SubscribeOwner
from fgapp.filters import RecipeFilterSet, IngredientSearchFilter
from fgapp.models import Recipe, Tag, Ingredient, FavoriteRecipe, ShoppingCart
from fgapp.pagination import CustomPageNumberPagination
from fgapp.serializers import (RecipeGetSerializer, RecipePostSerializer,
                               TagSerializer, IngredientSerializer,
                               SubscribeSerializer, FavoriteRecipeSerializer,
                               ShoppingCartSerializer)
from users.models import User, Subscribe


class ListModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CreateDeleteModelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class HealthAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        return Response({'message': 'success'})


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_cart = self.request.query_params.get('is_in_shopping_cart')
        if is_favorited is not None and int(is_favorited) == 1:
            favorites = FavoriteRecipe.objects.all().values_list(
                'recipe', flat=True
            )
            return queryset.filter(id__in=favorites)
        if is_in_cart is not None and int(is_in_cart) == 1:
            in_cart = ShoppingCart.objects.all().values_list(
                'recipe', flat=True
            )
            return queryset.filter(id__in=in_cart)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_serializer = RecipeGetSerializer(
            instance=serializer.instance
        )
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
    
    def partial_update(self, request, pk=None):
        recipe = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_serializer = RecipeGetSerializer(
            instance=serializer.instance
        )
        return Response(
            response_serializer.data, status=status.HTTP_200_OK
        )

    @action(detail=False, permission_classes = [permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user_cart = self.request.user.shopping_carts.all()
        recipe_id_list = user_cart.values_list('recipe', flat=True)
        ingr_amounts = RecipeIngredients.objects.filter(
            recipe__in=recipe_id_list).select_related('ingredient')
        unique_list=[]
        ingredients = {}
        for item in ingr_amounts:
            name = (
                item.ingredient.name + ' ('+
                item.ingredient.measurement_unit + ') - '
            ).capitalize()
            if item.ingredient.id in unique_list:
                ingredients[name] += item.amount
            else:
                ingredients[name] = item.amount
                unique_list.append(item.ingredient.id)
        cart_string = (
            'Список покупок.\n' + 'Выбрано рецептов: '
            + str(user_cart.count()) + '\n\n'
        )
        for ingredient, amount in ingredients.items():
            cart_string = (
                cart_string + ingredient + str(amount) + '\n'
            )
        return HttpResponse(cart_string, content_type='text/plain')


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class ShoppingCartViewSet(CreateDeleteModelViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = (RecipeAuthor,)

    def get_queryset(self):
        recipe_for_cart = get_object_or_404(
            Recipe, id=self.kwargs.get('recipe_id')
        )
        return recipe_for_cart

    def delete(self, request, recipe_id, format=None):
        recipe = get_object_or_404(
            Recipe, id=recipe_id
        )
        try:
            cart_item = get_object_or_404(
                ShoppingCart,
                user=self.request.user,
                recipe=recipe
            )
        except Http404:
            msg = f'Рецепт ({recipe.name}) уже отсутствует в списке покупок.'
            return Response(
                {'errors': msg}, status=status.HTTP_400_BAD_REQUEST
            )
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipeViewSet(CreateDeleteModelViewSet):
    serializer_class = FavoriteRecipeSerializer
    permission_classes = (RecipeAuthor,)

    def get_queryset(self):
        recipe_for_favorite = get_object_or_404(
            Recipe, id=self.kwargs.get('recipe_id')
        )
        return recipe_for_favorite

    def delete(self, request, recipe_id, format=None):
        recipe = get_object_or_404(
            Recipe, id=recipe_id
        )
        try:
            favorite = get_object_or_404(
                FavoriteRecipe,
                user=self.request.user,
                recipe=recipe
            )
        except Http404:
            msg = f'Рецепт ({recipe.name}) уже отсутствует в избранном.'
            return Response(
                {'errors': msg}, status=status.HTTP_400_BAD_REQUEST
            )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(ListModelViewSet):
    serializer_class = SubscribeSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (SubscribeOwner,)

    def get_queryset(self):
        subs_query = self.request.user.subscriber.all()
        subs_id_list = subs_query.values_list('subscribing', flat=True)
        return User.objects.filter(id__in=subs_id_list)


class SubscribeViewSet(CreateDeleteModelViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = (SubscribeOwner,)

    def get_queryset(self):
        author_for_subscribe = get_object_or_404(
            User, id=self.kwargs.get('user_id')
        )
        return author_for_subscribe

    def delete(self, request, user_id, format=None):
        author_for_unsubscribe = get_object_or_404(
            User, id=user_id
        )
        subscribe = get_object_or_404(
            Subscribe,
            user=self.request.user,
            subscribing=author_for_unsubscribe
        )
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
