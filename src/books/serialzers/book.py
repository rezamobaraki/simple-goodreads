from rest_framework import serializers

from books.models.book import Book
from books.serialzers.review import ReviewSerializer
from books.services.queries.bookmark import bookmark_count, is_bookmarked
from books.services.queries.review import average_rating, rating_count, rating_distribution, review_count


class BookListSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='api-v1:books:book:book-detail', lookup_field='pk')
    bookmark_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'bookmark_count')

    def get_bookmark_count(self, obj):
        return bookmark_count(book=obj)


class BookListWithBookmarksSerializer(BookListSerializer):
    """
    if user is authenticated, return is_bookmarked field
    (it is not a proper way) BUT it also can implement with removing is_bookmarked field from to_representation
    """
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'bookmark_count', 'is_bookmarked')

    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        return is_bookmarked(book=obj, user=user)


class BookDetailSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    rating_distribution = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'title', 'summary', 'review_count', 'rating_count',
            'average_rating', 'rating_distribution', 'reviews'
        )

    def get_review_count(self, obj):
        return review_count(book=obj)

    def get_rating_count(self, obj):
        return rating_count(book=obj)

    def get_average_rating(self, obj):
        return average_rating(book=obj)

    def get_rating_distribution(self, obj):
        return rating_distribution(book=obj)
