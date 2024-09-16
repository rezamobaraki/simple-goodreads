import factory
from books.models.book import Book

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    summary = factory.Faker('paragraph', nb_sentences=3)