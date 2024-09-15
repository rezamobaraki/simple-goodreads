from books.models import Book, Review


def review_count(*, book: Book) -> int:
    return Review.objects.filter(book=book).count()



def rating_count(*, book: Book) -> int:
    return Review.objects.filter(book=book).exclude(rating=None).count()