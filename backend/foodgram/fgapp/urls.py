from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from fgapp.views import (RecipeViewSet, TagsViewSet,
                         IngredientViewSet, ShoppingCartViewSet,
                         SubscribeViewSet,
                         SubscriptionsViewSet, FavoriteRecipeViewSet)

recipes_router = DefaultRouter()

recipes_router.register('tags', TagsViewSet)
recipes_router.register('ingredients', IngredientViewSet)
recipes_router.register('recipes', RecipeViewSet, basename='recipes')
recipes_router.register(
    r'recipes/(?P<recipe_id>[\d]+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shopping_cart'
)
recipes_router.register(
    r'recipes/(?P<recipe_id>[\d]+)/favorite',
    FavoriteRecipeViewSet,
    basename='favorite'
)
recipes_router.register(
    'users/subscriptions',
    SubscriptionsViewSet,
    basename='subscriptions'
)
recipes_router.register(
    r'users/(?P<user_id>[\d]+)/subscribe',
    SubscribeViewSet,
    basename='subscribe'
)

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(recipes_router.urls)),
    path('', include('djoser.urls')),
]
