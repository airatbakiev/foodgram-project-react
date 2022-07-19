from django.contrib import admin

from .models import Recipe, Tag, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'title', 'text', 'duration', 'pub_date')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('title',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'tagname', 'slug')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('tagname',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('tagname',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'product', 'unit', 'quantity')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('product',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('product',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
