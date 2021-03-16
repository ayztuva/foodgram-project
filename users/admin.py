from django.contrib import admin

from .models import User, Follow


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


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'user')
    search_fields = ('author', 'user')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
