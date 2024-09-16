from django.db.models import Count

from books.enums import ReviewRating
from books.models import Book, Review


def review_count(*, book: Book) -> int:
    return Review.objects.filter(book=book).aggregate(count=Count('id'))['count']


def rating_count(*, book: Book) -> int:
    return Review.objects.filter(book=book).exclude(rating=None).aggregate(count=Count('id'))['count']


from django.db.models import Avg
from django.db.models.functions import Round


def average_rating(*, book: Book) -> float:
    return Review.objects.filter(book=book).exclude(rating=None).aggregate(
        average=Round(Avg('rating'), precision=1)
    )['average']


def rating_distribution(*, book: Book) -> dict:
    distribution = {rating.name: 0 for rating in ReviewRating}

    rating_counts = Review.objects.filter(book=book).values('rating').annotate(count=Count('rating')).order_by('rating')
    for item in rating_counts:
        rating_name = ReviewRating(item['rating']).name
        distribution[rating_name] = item['count']

    return distribution


def is_reviewed(*, book: Book, user) -> bool:
    return Review.objects.filter(book=book, user=user).exists()
