import types

from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.response import Response

from . import serializers
from recipes.models import Favorite, Ingredient, Purchase
from users.models import Follow

_SUCCESS_RESPONSE = types.MappingProxyType({'success': True})
_UNSUCCESS_RESPONSE = types.MappingProxyType({'success': False})


class BaseInstanceView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(_SUCCESS_RESPONSE)
        return Response(_UNSUCCESS_RESPONSE)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_deleted = instance.delete()
        if is_deleted:
            return Response(_SUCCESS_RESPONSE)
        return Response(_UNSUCCESS_RESPONSE)


class FavoriteApiView(BaseInstanceView):
    queryset = Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        instance = get_object_or_404(
            queryset,
            user=self.request.user,
            recipe=self.kwargs['pk'],
        )
        self.check_object_permissions(self.request, instance)
        return instance


class FollowApiView(BaseInstanceView):
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        instance = get_object_or_404(
            queryset,
            user=self.request.user,
            author=self.kwargs['pk'],
        )
        self.check_object_permissions(self.request, instance)
        return instance


class PurchaseApiView(mixins.ListModelMixin, BaseInstanceView):
    queryset = Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        instance = get_object_or_404(
            queryset,
            user=self.request.user,
            recipe=self.kwargs['pk'],
        )
        self.check_object_permissions(self.request, instance)
        return instance


class IgredientApiView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)
