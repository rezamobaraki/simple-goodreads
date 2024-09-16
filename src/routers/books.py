from django.urls import include, path

app_name = 'books'

urlpatterns = [
    path('', include('books.urls.book', namespace='book'), name='book'),
]
