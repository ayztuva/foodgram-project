from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Recipe, Tag
from .service import add_ingredients_to_recipe


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        label=_('Теги'),
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    ingredients = forms.CharField(
        required=False,
        label=_('Ингредиенты'),
        widget=forms.TextInput(attrs={'id': 'nameIngredient'}),
    )

    class Meta:
        model = Recipe
        fields = (
            'title',
            'tags',
            'ingredients',
            'cooking_time',
            'text',
            'image',
        )
        labels = {
            'title': _('Название рецепта'),
            'cooking_time': _('Время приготовления'),
            'image': _('Загрузить фото'),
        }
        widgets = {
            'cooking_time': forms.TextInput(),
        }

    def clean_ingredients(self):
        ingredients = list(
            zip(
                self.data.getlist('nameIngredient'),
                self.data.getlist('valueIngredient'),
            ),
        )
        if not ingredients:
            raise forms.ValidationError(_('Отсутствуют ингредиенты'))

        ingredients_clean = []
        for name, quantity in ingredients:
            if int(quantity) < 1:
                raise forms.ValidationError(
                    _(f'Исправьте количество ингредиента "{name}"'))
            else:
                ingredients_clean.append({
                    'title': name,
                    'quantity': quantity,
                })
        return ingredients_clean

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        ingredients = self.cleaned_data['ingredients']
        self.cleaned_data['ingredients'] = []
        self.save_m2m()
        add_ingredients_to_recipe(self.instance, ingredients)

        return instance
