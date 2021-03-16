from django.conf import settings

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
]

urlpatterns += [
    path('', include('recipes.urls', namespace='recipes')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(  # type: ignore
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(  # type: ignore
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
