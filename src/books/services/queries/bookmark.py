from django.core.cache import cache

from accounts.models import User
from books.models import Book, Bookmark


def is_bookmarked(*, book: Book, user: User) -> bool:
    cache_key = f'is_bookmarked_{book.id}_{user.id}'
    bookmarked = cache.get(cache_key)
    if bookmarked is None:
        bookmarked = Bookmark.objects.filter(book=book, user=user).exists()
        cache.set(cache_key, bookmarked, timeout=60 * 15)  # Cache for 15 minutes
    return bookmarked


def bookmark_count(*, book: Book) -> int:
    cache_key = f'bookmark_count_{book.id}'
    count = cache.get(cache_key)
    if count is None:
        count = Bookmark.objects.filter(book=book).count()
        cache.set(cache_key, count, timeout=60 * 15)  # Cache for 15 minutes
    return count
