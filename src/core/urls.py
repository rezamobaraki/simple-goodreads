from django.contrib import admin
from django.urls import include, path

from common.views import health_check

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("api/v1/", include("routers.urls")),
    path('admin/', admin.site.urls),
]
