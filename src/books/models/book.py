from django.db import models
from django.utils.translation import gettext_lazy as _

from commons.models import BaseModel


class Book(BaseModel):
    title = models.CharField(max_length=200)
    summary = models.TextField()

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def __str__(self):
        return self.title

    @property
    def bookmark_count(self):
        return self.bookmarks.count()

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def rating_count(self):
        return self.reviews.exclude(rating__isnull=True).count()

    @property
    def average_rating(self):
        ratings = self.reviews.exclude(rating__isnull=True).values_list('rating', flat=True)
        return sum(ratings) / len(ratings) if ratings else 0

    @property
    def rating_distribution(self):
        distribution = {i: 0 for i in range(1, 6)}
        ratings = self.reviews.exclude(rating__isnull=True).values_list('rating', flat=True)
        for rating in ratings:
            distribution[rating] += 1
        return distribution
