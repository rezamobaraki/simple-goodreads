from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from books.enums import ReviewRating
from commons.models import BaseModel


class Review(BaseModel):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(ReviewRating.ONE_STAR), MaxValueValidator(ReviewRating.FIVE_STARS)
        ]
    )
    comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.email}'s review of {self.book.title}"
