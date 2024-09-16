from rest_framework import serializers

from books.enums import BookmarkStatus
from books.models import Book
from books.services.commands.book import bookmark_book
from books.services.queries.review import is_reviewed


class BookmarkSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), required=True)
    status = serializers.CharField(read_only=True)

    def validate(self, attrs):
        if is_reviewed(book=attrs['book'], user=attrs['user']):
            raise serializers.ValidationError('you can not bookmark a book that already reviewed')
        return attrs

    def create(self, validated_data):
        bookmark, created = bookmark_book(user=validated_data['user'], book=validated_data['book'])
        status = BookmarkStatus.CREATED if created else BookmarkStatus.DELETED
        return {
            'status': status,
            'book': validated_data['book'].id,
            'user': validated_data['user'].id
        }
