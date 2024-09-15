from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from books.permissions import IsAdminUserOrReadOnly
from books.serialzers.book import (
    BookDetailSerializer, BookListSerializer, BookListWithBookmarksSerializer
)
from books.serialzers.review import ReviewSerializer
from books.services.commands.book import toggle_bookmark
from books.services.queries.review import is_reviewed
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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, *args, **kwargs):
        user, book = request.user, self.get_object()
        if is_reviewed(book=book, user=user):
            return Response({"status": "Already reviewed"}, status=status.HTTP_400_BAD_REQUEST)

        bookmark = toggle_bookmark(user=user, book=book)
        status_message = "Bookmarked" if bookmark else "unBookmark"
        return Response({"status": status_message}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], serializer_class=ReviewSerializer)
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
