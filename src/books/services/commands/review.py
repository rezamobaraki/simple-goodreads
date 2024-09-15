from accounts.models import User
from books.models import Book, Review


def update_or_create_review(*, user: User, book: Book, rating: int, comment: str) -> tuple:
    review, created = Review.objects.update_or_create(
        user=user, book=book,
        defaults={'rating': rating, 'comment': comment}
    )
    return review, created
