from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from common.views import health_check

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("api/v1/", include("routers.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    debug_toolbar_urls = [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += debug_toolbar_urls
