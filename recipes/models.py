from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    units = models.CharField(max_length=12)

    class Meta:
        ordering = ('title',)
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    @classmethod
    def fill(cls, ingredients):
        for obj in ingredients:
            ingredient, created = cls.objects.get_or_create(
                title=obj.get('title'),
                units=obj.get('dimension')
            )

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, unique=True)
    cooking_time = models.PositiveIntegerField(
        verbose_name=_('Cooking time (minutes)'))
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='recipes')
    image = models.ImageField(blank=True, upload_to='media/recipes/')

    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        decimal_places=1, max_digits=6, validators=(MinValueValidator(1),))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            )
        ]
        verbose_name = _('recipe ingredient')
        verbose_name_plural = _('recipe ingredients')


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    color = models.CharField(max_length=25, default='white')

    class Meta:
        ordering = ('pk',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.title


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorites'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_favorite_recipe'
            )
        ]
        verbose_name = _('favorite')
        verbose_name_plural = _('favorites')
    
    def __str__(self):
        return f'{self.recipe.title} is {self.user.username} favorite'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_purchase'
            ),
        ]
        verbose_name = _('purchase')
        verbose_name_plural = _('purchases')

    def __str__(self):
        return f'{self.user.username} --> {self.recipe.name}'
