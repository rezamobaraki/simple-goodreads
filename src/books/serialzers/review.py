from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from books.enums import ReviewRating, ReviewStatus
from books.models import Book
from books.services.commands.book import review_book


class ReviewSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), required=True)
    rating = serializers.ChoiceField(choices=ReviewRating.choices, validators=[ReviewRating.validate_choice])
    status = serializers.CharField(read_only=True)
    comment = serializers.CharField(required=False)

    def validate(self, attrs):
        comment, rating = attrs.get('comment'), attrs.get('rating')
        if not comment or not rating:
            raise serializers.ValidationError('Comment or Rating are required', _("reviewed_book"))
        return attrs

    def create(self, validated_data):
        review, created = review_book(
            user=validated_data['user'], book=validated_data["book"], rating=validated_data['rating'],
            comment=validated_data['comment']
        )
        return {
            'status': ReviewStatus.CREATED if created else ReviewStatus.UPDATED,
            'review': {
                'id': review.id,
                'book': validated_data['book'].id,
                'user': validated_data['user'].id,
                'rating': validated_data['rating'],
                'comment': validated_data['comment']
            }
        }, created
