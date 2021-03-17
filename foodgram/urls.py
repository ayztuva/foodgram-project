from django.conf import settings
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import path, include


handler404 = 'foodgram.errors.page_not_found'
handler500 = 'foodgram.errors.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('about/', include('flatpages.urls')),
]

urlpatterns += [
    path('', include('recipes.urls', namespace='recipes')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
