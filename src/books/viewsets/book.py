from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from books.permissions import IsAdminUserOrReadOnly
from books.serialzers.book import (
    BookDetailSerializer, BookListSerializer, BookListWithBookmarksSerializer
)
from books.serialzers.bookmark import BookmarkSerializer
from books.serialzers.review import ReviewSerializer
from commons.viewsets import RetrieveListModelViewSet


class BookViewSet(RetrieveListModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'pk'

    def get_serializer_class(self):
        user = self.request.user
        if self.action == 'list' and user.is_authenticated:
            return BookListWithBookmarksSerializer
        if self.action == 'retrieve':
            return BookDetailSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], serializer_class=BookmarkSerializer)
    def bookmark(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(context={'book': book})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], serializer_class=ReviewSerializer)
    def review(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'book': book})
        serializer.is_valid(raise_exception=True)
        review, created = serializer.create(validated_data=serializer.validated_data)
        return Response({
            'status': 'review created' if created else 'review updated',
            'review': serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
