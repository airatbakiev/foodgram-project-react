from django.contrib import admin

from fgapp.models import (Recipe, RecipeIngredients, Tag, Ingredient,
                          RecipeTags, FavoriteRecipe, ShoppingCart)
from users.models import User, Subscribe


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'first_name', 'last_name', 'email'
    )
    search_fields = ('username',)
    list_filter = ('email', 'username')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'subscribing')
    search_fields = ('user', 'subscribing',)
    list_filter = ('user', 'subscribing',)


class IngredientsInLine(admin.TabularInline):
    model = RecipeIngredients
    min_num = 1


class TagsInLine(admin.TabularInline):
    model = RecipeTags


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientsInLine, TagsInLine]
    list_display = ('pk', 'author', 'name', 'text', 'pub_date')
    search_fields = ('name',)
    list_filter = ('tags', 'author', 'name')


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit', 'name')


class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')


class RecipeTagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag')
    search_fields = ('recipe', 'tag')


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeTags, RecipeTagsAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
