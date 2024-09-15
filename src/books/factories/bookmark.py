import factory
from books.models.bookmark import Bookmark
from accounts.factories.user import UserFactory
from books.factories.book import BookFactory

class BookmarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bookmark

    book = factory.SubFactory(BookFactory)
    user = factory.SubFactory(UserFactory)