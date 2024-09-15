from django.db.models import Avg, Count

from books.enums import ReviewRating
from books.models import Book, Review


def review_count(*, book: Book) -> int:
    return Review.objects.filter(book=book).aggregate(count=Count('id'))['count']


def rating_count(*, book: Book) -> int:
    return Review.objects.filter(book=book).exclude(rating=None).aggregate(count=Count('id'))['count']


def average_rating(*, book: Book) -> int:
    return Review.objects.filter(book=book).exclude(rating=None).aggregate(Avg('rating'))['rating__avg']


def rating_distribution(*, book: Book) -> dict:
    distribution = {rating.name: 0 for rating in ReviewRating}

    rating_counts = Review.objects.filter(book=book).values('rating').annotate(count=Count('rating')).order_by('rating')
    for item in rating_counts:
        rating_name = ReviewRating(item['rating']).name
        distribution[rating_name] = item['count']

    return distribution
