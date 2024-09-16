from accounts.models import User
from books.models import Book, Bookmark


def bookmark(*, book: Book, user: User) -> Bookmark:
    return Bookmark.objects.create(book=book, user=user)


def remove_bookmark(*, book: Book, user: User):
    Bookmark.objects.filter(book=book, user=user).delete()
