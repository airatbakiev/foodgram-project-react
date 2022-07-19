from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'first_name', 'last_name', 'role', 'email'
    )
    search_fields = ('username',)
    list_filter = ('email', 'username', 'role')


admin.site.register(User, UserAdmin)
