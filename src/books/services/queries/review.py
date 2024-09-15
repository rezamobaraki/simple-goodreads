from books.models import Book, Review


def get_review_count(*, book: Book) -> int:
    return Review.objects.filter(book=book).count()



def rating_count(*, book: Book) -> int:
    return Review.objects.filter(book=book).exclude(rating=None).count()