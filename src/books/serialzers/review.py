from rest_framework import serializers

from books.enums import ReviewRating
from books.models import Review
from books.services.commands.book import review_book


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    rating = serializers.ChoiceField(choices=ReviewRating.choices, validators=[ReviewRating.validate_choice])

    def validate(self, attrs):
        comment, rating = attrs.get('comment'), attrs.get('rating')
        if not comment or not rating:
            raise serializers.ValidationError('Comment or Rating are required')
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'comment')

    def create(self, validated_data):
        return review_book(
            user=validated_data['user'], book=self.context['book'], rating=validated_data['rating'],
            comment=validated_data['comment']
        )
