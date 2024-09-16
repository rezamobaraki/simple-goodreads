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
from commons.viewsets import CreateRetrieveListModelViewSet


class BookViewSet(CreateRetrieveListModelViewSet):
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ['bookmark', 'review']:
            context['user'] = self.request.user
            context['book'] = self.get_object()
        return context

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], serializer_class=BookmarkSerializer)
    def bookmark(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        _, created = serializer.save()
        return Response({"status": "Bookmarked" if created else "Unbookmarked"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], serializer_class=ReviewSerializer, permission_classes=[IsAuthenticated])
    def review(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        context['book'] = self.get_object()
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        review, created = serializer.create(validated_data=serializer.data)
        Response({
            'status': 'review created' if created else 'review updated',
            'review': serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
