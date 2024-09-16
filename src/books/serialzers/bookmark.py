from rest_framework import serializers

from books.enums import BookmarkStatus
from books.services.commands.book import bookmark_book
from books.services.queries.review import is_reviewed


class BookmarkSerializer(serializers.Serializer):
    status = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        attrs['book'] = self.context['book']
        if is_reviewed(book=attrs['user'], user=attrs['book']):
            raise serializers.ValidationError('Already reviewed')
        return attrs

    def create(self, validated_data):
        bookmark, created = bookmark_book(user=validated_data['user'], book=validated_data['book'])
        validated_data['status'] = BookmarkStatus.CREATED if created else BookmarkStatus.DELETED
        return validated_data
