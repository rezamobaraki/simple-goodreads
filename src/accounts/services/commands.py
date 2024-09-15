from django.contrib.auth import get_user_model

User = get_user_model()


def auth_create_user(*, email: str, password: str) -> User:
    user, created = User.objects.get_or_create(email=email)
    if created:
        user.set_password(password)
        user.save()
    else:
        if not user.check_password(password):
            return None
    return user
