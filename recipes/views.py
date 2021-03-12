from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .mixins import TagContextMixin

User = get_user_model()


def index(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()

    return render(
        request,
        'index.html',
        {
            'page': page,
            'paginator':paginator,
            'tags': tags
        }
    )
