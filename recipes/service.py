import io

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from reportlab.pdfgen.canvas import Canvas

from .models import Ingredient, Recipe, RecipeIngredient


def add_ingredients_to_recipe(recipe, ingredients):
    Recipe.ingredients.through.objects.bulk_create(
        [
            Recipe.ingredients.through(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient,
                    title=ingredient['title'],
                ),
                quantity=ingredient['quantity'],
            ) for ingredient in ingredients
        ],
    )


def generate_pdf(user):
    buffer = io.BytesIO()
    canvas = Canvas(buffer, bottomup=0)

    title = 'Список покупок | Foodgram'
    canvas.setTitle(title)
    x_coordinate = 50
    y_coordinate = 50

    font_size = 18
    canvas.setFont('Montserrat', font_size)
    canvas.drawString(x_coordinate, y_coordinate, title)

    font_size = 14
    dy = 50
    canvas.setFont('Montserrat', font_size)
    canvas.drawString(x_coordinate, y_coordinate + dy, 'Продукты:')

    y_coordinate = 130
    dy = 25
    font_size = 12
    canvas.setFont('Montserrat', font_size)

    ingredients = RecipeIngredient.objects.filter(
        recipe__in_purchases__user=user,
    ).values(
        'ingredient__title',
        'ingredient__dimension',
    ).annotate(quantity=Sum('quantity'))

    for ingredient in ingredients:
        line = '{0} {1} {2}'.format(
            ingredient['ingredient__title'],
            ingredient['quantity'],
            ingredient['ingredient__dimension'],
        )
        canvas.drawString(x_coordinate, y_coordinate, line)
        y_coordinate += dy

    canvas.showPage()
    canvas.save()
    buffer.seek(0)

    return buffer
