from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


@transaction.atomic
def auth_create_user(*, email: str, password: str) -> User:
    user, created = User.objects.get_or_create(email=email)
    if created:
        user.set_password(password)
        user.save()
    elif not user.check_password(password):
        return None
    return user

