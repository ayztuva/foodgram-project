# Generated by Django 3.1.6 on 2021-03-13 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'favorite', 'verbose_name_plural': 'favorites'},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'verbose_name': 'purchase', 'verbose_name_plural': 'purchases'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'recipe', 'verbose_name_plural': 'recipes'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'recipe ingredient', 'verbose_name_plural': 'recipe ingredients'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('pk',), 'verbose_name': 'tag', 'verbose_name_plural': 'tags'},
        ),
        migrations.AlterField(
            model_name='purchase',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_purchases', to='recipes.recipe'),
        ),
    ]