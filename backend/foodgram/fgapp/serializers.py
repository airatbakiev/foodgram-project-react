from base64 import b64decode
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
import uuid

from .models import (Recipe, Ingredient, Tag, RecipeIngredients, RecipeTags,
                     FavoriteRecipe, ShoppingCart)
from users.models import User, Subscribe
from users.serializers import CustomUserSerializer


class CustomImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            return ContentFile(
                b64decode(imgstr), name=uuid.uuid4().hex + "." + ext
            )
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class GetIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class PostIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if data['amount'] <= 0:
            raise serializers.ValidationError(
                'Количество каждого ингредиента должно быть больше нуля.'
            )
        return data


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingr_amounts = RecipeIngredients.objects.filter(
            recipe=obj
        )
        serializer = GetIngredientsSerializer(ingr_amounts, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        request = self.context.get('request', )
        if not request or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request', )
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class RecipePostSerializer(serializers.ModelSerializer):
    ingredients = PostIngredientsSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = CustomImageField(required=False)

    class Meta:
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )
        model = Recipe

    def ingredients_tags_create(self, recipe, ingredients_data, tags_id_list):
        tags_objs = [
            RecipeTags(recipe=recipe, tag=tag_id)
            for tag_id in tags_id_list
        ]
        RecipeTags.objects.bulk_create(tags_objs)
        ingr_objs = []
        for ingredient in ingredients_data:
            current_ingredient = get_object_or_404(
                Ingredient,
                id=ingredient['ingredient']
            )
            amount = ingredient['amount']
            ingr_objs.append(
                RecipeIngredients(
                    ingredient=current_ingredient,
                    recipe=recipe,
                    amount=amount
                )
            )
        RecipeIngredients.objects.bulk_create(ingr_objs)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_id_list = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.ingredients_tags_create(recipe, ingredients_data, tags_id_list)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_id_list = validated_data.pop('tags')
        RecipeTags.objects.filter(recipe=instance).delete()
        RecipeIngredients.objects.filter(recipe=instance).delete()
        self.ingredients_tags_create(instance, ingredients_data, tags_id_list)
        # instance.image = validated_data.get('image', instance.image)
        # instance.name = validated_data.get('name', instance.name)
        # instance.text = validated_data.get('text', instance.text)
        # instance.cooking_time = validated_data.get(
        #     'cooking_time', instance.cooking_time
        # )
        # instance.save()
        return super().update(instance, validated_data)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if not data['ingredients']:
            raise serializers.ValidationError(
                'Для создания рецепта заполните ингредиенты.'
            )
        if not data['tags']:
            raise serializers.ValidationError(
                'Для создания рецепта заполните теги.'
            )
        if data['cooking_time'] <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше нуля.'
            )
        unique_list = []
        for ingr in data['ingredients']:
            if ingr['ingredient'] in unique_list:
                raise serializers.ValidationError(
                    'Устраните дублирующиеся ингредиенты.'
                )
            else:
                unique_list.append(ingr['ingredient'])
        return data


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipeSerializer(ShortRecipeSerializer):

    def create(self, validated_data):
        recipe_for_favorite = get_object_or_404(
            Recipe,
            id=self.context['request'].parser_context['kwargs']['recipe_id']
        )
        FavoriteRecipe.objects.create(
            user=self.context['request'].user,
            recipe=recipe_for_favorite
        )
        return recipe_for_favorite

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        recipe = self.context['request'].parser_context['kwargs']['recipe_id']
        user = self.context['request'].user
        if FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists():
            recipe_name = Recipe.objects.get(id=recipe).name
            raise serializers.ValidationError(
                f'Рецепт ({recipe_name}) уже добавлен в избранное.'
            )
        return data


class ShoppingCartSerializer(ShortRecipeSerializer):

    def create(self, validated_data):
        recipe_for_cart = get_object_or_404(
            Recipe,
            id=self.context['request'].parser_context['kwargs']['recipe_id']
        )
        ShoppingCart.objects.create(
            user=self.context['request'].user,
            recipe=recipe_for_cart
        )
        return recipe_for_cart

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        recipe = self.context['request'].parser_context['kwargs']['recipe_id']
        user = self.context['request'].user
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            recipe_name = Recipe.objects.get(id=recipe).name
            raise serializers.ValidationError(
                f'Рецепт ({recipe_name}) уже добавлен в Ваш список покупок.'
            )
        return data


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request', )
        if not request or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=request.user,
            subscribing=obj
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        else:
            recipes = obj.recipes.all()
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def create(self, validated_data):
        author_for_subscribe = get_object_or_404(
            User,
            id=self.context['request'].parser_context['kwargs']['user_id']
        )
        Subscribe.objects.create(
            user=self.context['request'].user,
            subscribing=author_for_subscribe
        )
        return author_for_subscribe

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        subs_id = self.context['request'].parser_context['kwargs']['user_id']
        subs = get_object_or_404(User, id=subs_id)
        user = self.context['request'].user
        if user == subs:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if Subscribe.objects.filter(user=user, subscribing=subs).exists():
            raise serializers.ValidationError(
                f'Вы уже подписаны на автора {subs}.'
            )
        return data
