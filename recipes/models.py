from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    dimension = models.CharField(max_length=12)

    class Meta:
        ordering = ('title',)
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'

    @classmethod
    def fill(cls, ingredients):
        for obj in ingredients:
            ingredient, created = cls.objects.get_or_create(
                title=obj.get('title'),
                dimension=obj.get('dimension')
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
    cooking_time = models.PositiveIntegerField(
        verbose_name='Cooking time (minutes)')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='recipes')
    image = models.ImageField(blank=True, upload_to='recipes/')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'recipe ingredient'
        verbose_name_plural = 'recipe ingredients'


class Tag(models.Model):
    class TagChoices(models.TextChoices):
        BREAKFAST = 'breakfast', 'Завтрак'
        LUNCH = 'lunch', 'Обед'
        DINNER = 'dinner', 'Ужин'

    class ColorChoices(models.TextChoices):
        GREEN = 'green', 'Зеленый'
        ORANGE = 'orange', 'Оранжевый'
        PURPLE = 'purple', 'Фиолетовый'

    title = models.CharField(
        choices=TagChoices.choices,
        default=TagChoices.LUNCH,
        unique=True,
        max_length=10,
    )
    color = models.CharField(
        choices=ColorChoices.choices,
        default=ColorChoices.GREEN,
        unique=True,
        max_length=10,
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

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
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'

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
        related_name='in_purchases',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_purchase'
            ),
        ]
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'

    def __str__(self):
        return f'{self.user.username} --> {self.recipe.title}'
