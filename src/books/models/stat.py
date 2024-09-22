from django.db import models
from django.forms import JSONField
from django.utils.translation import gettext_lazy as _

from books.models import Book
from books.services.queries.review import average_rating, rating_count, rating_distribution, review_count
from commons.models import BaseModel


class BookStat(BaseModel):
    book = models.OneToOneField("Book", on_delete=models.CASCADE, related_name='stat')
    review_count = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    rating_distribution = JSONField(default=dict)

    class Meta:
        verbose_name = _('book stat')
        verbose_name_plural = _('book stats')

    def __str__(self):
        return f"Stat of {self.book.title}"

    @classmethod
    def update_or_create_stat(cls, book: Book):
        stats, created = cls.objects.get_or_create(book=book)
        stats.review_count = review_count(book=book)
        stats.rating_count = rating_count(book=book)
        stats.average_rating = average_rating(book=book)
        stats.rating_distribution = rating_distribution(book=book)
        stats.save()
        return stats

    @classmethod
    def get_or_calculate_stats(cls, book: Book):
        try:
            return cls.objects.get(book=book)
        except cls.DoesNotExist:
            return cls.update_or_create_stat(book=book)
