from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from books.models import Book, Bookmark


class BookmarkSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Bookmark
        fields = ('book', 'user')

    def create(self, validated_data):
        return Bookmark.objects.create(**validated_data)

    def delete(self, validated_data):
        return Bookmark.objects.delete(**validated_data)