from django.contrib import admin

from .models import Recipe, Tag, Ingredient, RecipeIngredients


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'pub_date')
    search_fields = ('title',)
    list_filter = ('tags', 'author',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tagname', 'slug')
    search_fields = ('tagname',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'unit')
    search_fields = ('product',)
    list_filter = ('unit',)
    empty_value_display = '-пусто-'


class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'quantity')
    search_fields = ('recipe', 'ingredient')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
