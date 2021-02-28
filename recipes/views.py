from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404

from .models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()


def index(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        return render(request, 'indexAuth.html', {'page': page})
    return render(request, 'indexNotAuth.html', {'page': page})
