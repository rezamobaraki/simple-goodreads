from rest_framework.routers import SimpleRouter

from books.viewsets.book import BookViewSet

app_name = 'books'

router = SimpleRouter()

router.register(r'', BookViewSet, basename='book')

urlpatterns = router.urls
