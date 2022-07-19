from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'pk', 'username', 'first_name', 'last_name', 'role', 'email'
    )
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('username',)
    # Добавляем возможность фильтрации по роли
    list_filter = ('role',)


admin.site.register(User, UserAdmin)
