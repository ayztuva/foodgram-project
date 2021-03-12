from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'role'
    )
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)
