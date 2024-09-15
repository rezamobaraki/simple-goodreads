from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from books.permissions import IsAdminUserOrReadOnly
from books.serialzers.book import (
    BookBookmarkSerializer, BookDetailSerializer, BookListSerializer, BookListWithBookmarksSerializer
)
from commons.viewsets import RetrieveListModelViewSet


class BookViewSet(RetrieveListModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user
        if self.action == 'list' and user.is_authenticated:
            return BookListWithBookmarksSerializer
        if self.action == 'retrieve':
            return BookDetailSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=['post'], serializer_class=BookBookmarkSerializer,
            permission_classes=[IsAuthenticated])
    def bookmark(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        context["book"] = self.get_object()
        serializer = self.get_serializer(data={'user': request.user}, context=context)
        serializer.is_valid(raise_exception=True)
        created = serializer.create(serializer.validated_data)
        if created:
            return Response({'status': 'Bookmark created'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'Bookmark removed'}, status=status.HTTP_200_OK)
