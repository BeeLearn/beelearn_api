from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path("martor/", include("martor.urls")),
    path("grappelli/", include("grappelli.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    re_path(r"^_nested_admin/", include("nested_admin.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("beelearn.api_urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
