from rest_framework.routers import SimpleRouter

from books.viewsets import BookViewSet

app_name = 'book'

router = SimpleRouter()

router.register(r'', BookViewSet, basename='book')

urlpatterns = router.urls
