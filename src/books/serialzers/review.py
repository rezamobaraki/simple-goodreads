from rest_framework import serializers

from books.enums import ReviewRating
from books.models.review import Review
from books.services.commands.bookmark import remove_bookmark
from books.services.commands.review import update_or_create_review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    rating = serializers.ChoiceField(choices=ReviewRating.choices, validators=[ReviewRating.validate_choice])

    class Meta:
        model = Review
        fields = ('user', 'rating', 'comment', 'created_at')

    def create(self, validated_data):
        user, book = validated_data['user'], validated_data['book']
        remove_bookmark(book=book, user=user)
        return update_or_create_review(user=user, book=book, **validated_data)
