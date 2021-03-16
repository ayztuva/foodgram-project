from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new/', views.RecipeCreateView.as_view(), name='new'),
    path('follow/', views.FollowView.as_view(), name='follow'),
    path('favorites/', views.FavoriteView.as_view(), name='favorites'),
    path('purchases/', views.PurchaseView.as_view(), name='purchases'),
    path(
        'purchases/download/',
        views.DownloadPurchasesListView.as_view(),
        name='purchases_download',
    ),
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
    path(
        '<str:username>/<int:pk>/',
        views.RecipeView.as_view(),
        name='recipe',
    ),
    path(
        '<str:username>/<int:pk>/edit/',
        views.RecipeUpdateView.as_view(),
        name='recipe_edit',
    ),
    path(
        '<str:username>/<int:pk>/delete/',
        views.RecipeDeleteView.as_view(),
        name='recipe_delete',
    ),
]
