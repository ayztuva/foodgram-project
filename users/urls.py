from django.contrib.auth.views import LoginView
from django.urls import path

from . import views
from . forms import UserLoginForm

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'login/',
        LoginView.as_view(authentication_form=UserLoginForm),
        name='login',
    ),
]
