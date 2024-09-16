import factory

from accounts.factories.user import UserFactory
from books.factories.book import BookFactory
from books.models.review import Review


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    book = factory.SubFactory(BookFactory)
    user = factory.SubFactory(UserFactory)
    rating = factory.Iterator([1, 2, 3, 4, 5])
    comment = factory.Faker('paragraph', nb_sentences=2)
