from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'USR', _('User')
        ADMIN = 'ADM', _('Admin')
    
    email = models.EmailField(blank=False, unique=True)
    username = models.CharField(blank=False, unique=True, max_length=50)
    role =  models.CharField(
        default=Role.USER, choices=Role.choices, max_length=8)


    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser


class Follow(models.Model):
    author = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='follow', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'user'), name='unique_following')
        ]
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return f'user: {self.user.username}, author: {self.author.username}'
