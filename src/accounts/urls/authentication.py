from rest_framework.routers import SimpleRouter

from accounts.viewsets.authentication import AuthenticationViewSet

app_name = 'authentication'

router = SimpleRouter()

router.register(r'', AuthenticationViewSet, basename='authentication')

urlpatterns = router.urls
