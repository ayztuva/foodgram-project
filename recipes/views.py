from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django_filters.views import BaseFilterView
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .filters import TaggedRecipeFilterSet
from .forms import RecipeForm
from .permissions import AdminAuthorPermission
from .service import generate_pdf
from .mixins import TagContextMixin
from .models import (
    Recipe,
    Favorite,
    Purchase,
)

User = get_user_model()


class IndexView(TagContextMixin, BaseFilterView, ListView):
    """Main page with all recipes"""

    model = Recipe
    template_name = 'recipes/index.html'
    paginate_by = 6
    filterset_class = TaggedRecipeFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                is_in_favorites=Exists(
                    Favorite.objects.filter(
                        user=self.request.user,
                        recipe=OuterRef('pk'),
                    ),
                ),
            ).annotate(
                is_in_purchases=Exists(
                    Purchase.objects.filter(
                        user=self.request.user,
                        recipe=OuterRef('pk'),
                    ),
                ),
            )
        return queryset


class FollowView(LoginRequiredMixin, ListView):
    """List of following users"""

    model = User
    template_name = 'recipes/follow.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            followers__user=self.request.user).order_by('-id')


class FavoriteView(
        TagContextMixin,
        LoginRequiredMixin,
        BaseFilterView,
        ListView):
    """User favorite recipes"""

    model = Recipe
    template_name = 'recipes/favorites.html'
    paginate_by = 6
    filterset_class = TaggedRecipeFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(in_favorites__user=self.request.user)


class ProfileView(TagContextMixin, BaseFilterView, ListView):
    """Profile page"""

    model = Recipe
    template_name = 'recipes/profile.html'
    paginate_by = 6
    filterset_class = TaggedRecipeFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        is_follower = False
        if self.request.user.is_authenticated:
            if self.request.user.followers.filter(author=author).exists():
                is_follower = True
        context.update(
            {
                'user_is_follower': is_follower,
                'author': author,
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        author = get_object_or_404(User, username=self.kwargs['username'])
        return queryset.filter(author=author)


class RecipeView(DetailView):
    """Page with specific recipe"""

    model = Recipe
    template_name = 'recipes/recipe.html'


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Create new recipe"""

    model = Recipe
    template_name = 'recipes/add_recipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('recipes:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, AdminAuthorPermission, UpdateView):
    """Edit recipe"""

    model = Recipe
    template_name = 'recipes/add_recipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('recipes:index')


class RecipeDeleteView(LoginRequiredMixin, AdminAuthorPermission, DeleteView):
    """Delete recipe"""

    model = Recipe
    success_url = reverse_lazy('recipes:purchases')


class PurchaseView(LoginRequiredMixin, ListView):
    """User's purchase page with chosen recipes"""

    model = Recipe
    template_name = 'recipes/purchases.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(in_purchases__user=self.request.user)


class DownloadPurchasesListView(View):
    """Download shopping list"""

    def get(self, request, *args, **kwargs):
        pdf = generate_pdf(request.user)

        return FileResponse(
            pdf,
            as_attachment=True,
            filename='purchases.pdf',
        )
