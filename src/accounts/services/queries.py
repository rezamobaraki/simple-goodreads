from django.contrib.auth import get_user_model

User = get_user_model()


def authenticate_user(*, email: str, password: str) -> User:
    user = User.objects.filter(email=email).first()
    if user and user.check_password(password):
        return user
    return None
