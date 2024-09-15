from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.services.commands import auth_create_user

User = get_user_model()


class AuthenticationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = auth_create_user(email=validated_data["email"], password=validated_data["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        refresh_token = TokenObtainPairSerializer.get_token(user)
        access_token = str(refresh_token.access_token)
        return {'user': user, 'access_token': access_token}
