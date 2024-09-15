from books.models import Book
from books.permissions import IsAdminUserOrReadOnly
from books.serialzers.book import BookDetailSerializer, BookListSerializer, BookListWithBookmarksSerializer
from commons.viewsets import RetrieveListModelViewSet


class BookViewSet(RetrieveListModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user
        if self.action == 'list' and user.is_authenticated:
            return BookListWithBookmarksSerializer
        elif self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer

    # @action(detail=True, methods=['post'], serializer_class=BookmarkSerializer, permission_classes=[IsAuthenticated])
    # def bookmark(self, request, *args, **kwargs):
    #     book = self.get_object()
    #     serializer = self.get_serializer(data={'book': book.pk})
    #     if serializer.is_valid():
    #         bookmark, created = Bookmark.objects.get_or_create(
    #             book=book,
    #             user=request.user
    #         )
    #         if created:
    #             return Response({'status': 'bookmarked'}, status=status.HTTP_201_CREATED)
    #         else:
    #             bookmark.delete()
    #             return Response({'status': 'unbookmarked'}, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
