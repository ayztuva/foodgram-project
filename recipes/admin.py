from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'units')
    search_fields = ('title',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'pub_date',
        'slug',
        'text',
        'cooking_time',
    )
    search_fields = ('title', 'author', 'slug')
    list_filter = ('pub_date',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Tag, TagAdmin)
