from django.core.cache import cache
from django.db.models import Avg, Count
from django.db.models.functions import Round

from books.enums import ReviewRating
from books.models import Book, Review


def review_count(*, book: Book) -> int:
    cache_key = f'review_count_{book.id}'
    count = cache.get(cache_key)
    if count is None:
        count = Review.objects.filter(book=book).aggregate(count=Count('id'))['count']
        cache.set(cache_key, count, timeout=60*15)  # Cache for 15 minutes
    return count


def rating_count(*, book: Book) -> int:
    cache_key = f'rating_count_{book.id}'
    count = cache.get(cache_key)
    if count is None:
        count = Review.objects.filter(book=book).exclude(rating=None).aggregate(count=Count('id'))['count']
        cache.set(cache_key, count, timeout=60*15)  # Cache for 15 minutes
    return count


def average_rating(*, book: Book) -> float:
    cache_key = f'average_rating_{book.id}'
    average = cache.get(cache_key)
    if average is None:
        average = Review.objects.filter(book=book).exclude(rating=None).aggregate(
            average=Round(Avg('rating'), precision=1)
        )['average']
        cache.set(cache_key, average, timeout=60*15)  # Cache for 15 minutes
    return average


def rating_distribution(*, book: Book) -> dict:
    cache_key = f'rating_distribution_{book.id}'
    distribution = cache.get(cache_key)
    if distribution is None:
        distribution = {rating.name: 0 for rating in ReviewRating}
        rating_counts = Review.objects.filter(book=book).values('rating').annotate(count=Count('rating')).order_by('rating')
        for item in rating_counts:
            rating_name = ReviewRating(item['rating']).name
            distribution[rating_name] = item['count']
        cache.set(cache_key, distribution, timeout=60*15)  # Cache for 15 minutes
    return distribution


def is_reviewed(*, book: Book, user) -> bool:
    cache_key = f'is_reviewed_{book.id}_{user.id}'
    reviewed = cache.get(cache_key)
    if reviewed is None:
        reviewed = Review.objects.filter(book=book, user=user).exists()
        cache.set(cache_key, reviewed, timeout=60*15)  # Cache for 15 minutes
    return reviewed