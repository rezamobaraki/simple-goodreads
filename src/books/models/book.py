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
