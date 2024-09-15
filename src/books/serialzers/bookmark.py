from rest_framework import serializers

from books.services.commands.bookmark import bookmark, remove_bookmark
from books.services.queries.bookmark import is_bookmarked
from books.services.queries.review import is_reviewed


class BookmarkSerializer(serializers.Serializer):
    def validate(self, attrs):
        user, book = self.context['user'], self.context['book']
        if is_reviewed(book=book, user=user):
            raise serializers.ValidationError('Already reviewed')
        return attrs

    def create(self, validated_data):
        user, book = self.context['user'], self.context['book']
        created = True
        if is_bookmarked(book=book, user=user):
            return remove_bookmark(book=book, user=user), not created
        return bookmark(user=user, book=book), created
