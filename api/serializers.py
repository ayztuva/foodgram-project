from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Favorite, Ingredient, Purchase, Recipe
from users.models import Follow

User = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        queryset=Recipe.objects.all(),
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ('user', 'id')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='author',
        queryset=User.objects.all(),
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ('user', 'id')


class PurchaseSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        queryset=Recipe.objects.all(),
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Purchase
        fields = ('user', 'id')


class IngredientSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = ('title', 'dimension')
