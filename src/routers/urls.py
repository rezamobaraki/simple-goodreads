from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

app_name = "api-v1"

schema_view = get_schema_view(
    openapi.Info(
        title="GoodReads APIs",
        default_version='v1',
        description="Simplified model of GoodReads APIs with Django",
        contact=openapi.Contact(email="rezam578@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
swagger = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

urlpatterns = [
    path("accounts/", include("routers.accounts", namespace="accounts"), name="accounts"),
    path("books/", include("routers.books", namespace="books"), name="books"),
]

urlpatterns += swagger
