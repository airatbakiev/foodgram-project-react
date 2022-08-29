from django.http import HttpResponse

from fgapp.models import RecipeIngredients


def get_shopping_cart(user):
    '''Загрузка файла со списком покупок'''
    user_cart = user.shopping_carts.all()
    recipe_id_list = user_cart.values_list('recipe', flat=True)
    ingr_amounts = RecipeIngredients.objects.filter(
        recipe__in=recipe_id_list).select_related('ingredient')
    unique_list = []
    ingredients = {}
    for item in ingr_amounts:
        name = (
            item.ingredient.name + ' ('
            + item.ingredient.measurement_unit + ') - '
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
