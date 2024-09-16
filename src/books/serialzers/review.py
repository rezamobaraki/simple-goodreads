from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from books.enums import ReviewRating
from books.models import Book, Review
from books.services.commands.book import review_book


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), required=True)
    rating = serializers.ChoiceField(choices=ReviewRating.choices, validators=[ReviewRating.validate_choice])

    def validate(self, attrs):
        comment, rating = attrs.get('comment'), attrs.get('rating')
        if not comment or not rating:
            raise serializers.ValidationError('Comment or Rating are required', _("reviewed_book"))
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'user', 'book', 'rating', 'comment')

    def create(self, validated_data):
        return review_book(
            user=validated_data['user'], book=validated_data["book"], rating=validated_data['rating'],
            comment=validated_data['comment']
        )
