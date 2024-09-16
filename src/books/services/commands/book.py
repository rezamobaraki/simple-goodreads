from accounts.models import User
from books.models import Book
from books.services.commands.bookmark import bookmark, remove_bookmark
from books.services.commands.review import update_or_create_review
from books.services.queries.bookmark import is_bookmarked


def bookmark_book(*, user: User, book: Book):
    created = True
    if is_bookmarked(book=book, user=user):
        return remove_bookmark(book=book, user=user), not created
    return bookmark(user=user, book=book), created


def review_book(*, user: User, book: Book, rating: int, comment: str):
    remove_bookmark(book=book, user=user)
    return update_or_create_review(user=user, book=book, rating=rating, comment=comment)
