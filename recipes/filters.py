from django_filters import FilterSet
from django_filters.filters import ModelMultipleChoiceFilter

from .models import Recipe, Tag


class TaggedRecipeFilterSet(FilterSet):
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__title',
        to_field_name='title',
    )

    class Meta:
        model = Recipe
        fields = ('tags',)
