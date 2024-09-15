from rest_framework import serializers

from books.models.book import Book
from books.serialzers.review import ReviewSerializer
from books.services.queries.bookmark import is_bookmarked


class BookListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='book-detail', lookup_field='id')
    bookmark_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'bookmark_count')


class BookListWithBookmarksSerializer(BookListSerializer):
    """
    if user is authenticated, return is_bookmarked field
    (it is not a proper way) BUT it also can implement with removing is_bookmarked field from to_representation
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'bookmark_count', 'is_bookmarked')

    def get_is_bookmarked(self, obj):
        return is_bookmarked(book=obj, user=self.validated_data['user'])


class BookDetailSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    rating_distribution = serializers.DictField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'title', 'summary', 'review_count', 'rating_count',
            'average_rating', 'rating_distribution', 'reviews'
        )
