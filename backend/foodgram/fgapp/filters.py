from django_filters import rest_framework as filters

from fgapp.models import Tag, Ingredient
from users.models import User


class RecipeFilterSet(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        label='tags',
        queryset=Tag.objects.all())
    author = filters.ModelChoiceFilter(queryset=User.objects.all())


class IngredientSearchFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
