from rest_framework import serializers

from books.enums import ReviewRating
from books.models import Review
from books.services.commands.bookmark import remove_bookmark
from books.services.commands.review import update_or_create_review  # Custom function


class ReviewSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    rating = serializers.ChoiceField(choices=ReviewRating.choices, validators=[ReviewRating.validate_choice])

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'comment')

    def create(self, validated_data):
        user = validated_data['user']
        book = self.context['book']
        remove_bookmark(book=book, user=user)
        return update_or_create_review(user=user, book=book, **validated_data)
