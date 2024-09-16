from django.db import models
from commons.models import BaseModel

class Bookmark(BaseModel):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='bookmarks')

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.email}'s bookmark of {self.book.title}"