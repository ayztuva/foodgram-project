from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Purchase,
    Recipe,
    RecipeIngredient,
    Tag,
)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    search_fields = ('title',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def count_favorites(self, obj):
        return obj.in_favorites.count()

    count_favorites.short_description = 'favorites'

    list_display = ('pk', 'title', 'author', 'count_favorites')
    exclude = ('tags',)
    search_fields = ('title', 'author__username')
    list_filter = ('pub_date',)
    inlines = (IngredientInline, TagInline)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'quantity')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'color')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    def count_purchares(self, obj):
        return obj.recipe.ingredients.count()
    count_purchares.short_description = 'items'

    list_display = ('pk', 'user', 'count_purchares')
