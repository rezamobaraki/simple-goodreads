from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from books.serialzers.review import ReviewSerializer


class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        user = self.request.user

        # Remove bookmark if exists
        user.bookmarked_books.remove(book)

        # Update or create review
        review, created = Review.objects.update_or_create(
            user=user, book=book,
            defaults={'rating': serializer.validated_data.get('rating'),
                      'comment': serializer.validated_data.get('comment')}
        )
