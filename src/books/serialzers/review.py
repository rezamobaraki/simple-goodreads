from rest_framework import serializers

from books.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ('user', 'rating', 'comment', 'created_at')