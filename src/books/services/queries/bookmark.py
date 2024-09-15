from accounts.models import User
from books.models import Book, Bookmark


def is_bookmarked(*, book: Book, user: User) -> bool:
    return Bookmark.objects.filter(book=book, user=user).exists()


def get_bookmark_count(*, book: Book) -> int:
    return Bookmark.objects.filter(book=book).count()
