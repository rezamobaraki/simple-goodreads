from rest_framework import serializers

from books.models.book import Book
from books.models.bookmark import Bookmark
from books.serialzers.review import ReviewSerializer


class BookListSerializer(serializers.ModelSerializer):
    bookmark_count = serializers.IntegerField(read_only=True)
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'bookmark_count', 'is_bookmarked']

    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Bookmark.objects.filter(user=user, book=obj).exists()
        return False


class BookDetailSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    rating_distribution = serializers.DictField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'summary', 'review_count', 'rating_count', 'average_rating', 'rating_distribution',
                  'reviews']
