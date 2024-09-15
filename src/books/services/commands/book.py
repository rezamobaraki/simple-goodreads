from accounts.models import User
from books.models import Book
from books.services.commands.bookmark import bookmark, remove_bookmark
from books.services.queries.bookmark import is_bookmarked


def toggle_bookmark(*, user: User, book: Book):
    if is_bookmarked(book=book, user=user):
        return remove_bookmark(book=book, user=user)
    return bookmark(book=book, user=user)
