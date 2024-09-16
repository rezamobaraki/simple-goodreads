from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.services.commands import auth_create_user

User = get_user_model()


class AuthenticationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True, validators=[EmailValidator])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = auth_create_user(email=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        refresh_token = TokenObtainPairSerializer.get_token(user)
        access_token = str(refresh_token.access_token)
        return {"access_token": access_token, "refresh_token": str(refresh_token)}
