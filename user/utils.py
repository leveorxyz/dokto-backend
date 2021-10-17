from django.contrib.auth.hashers import make_password

from .models import User, UserLanguage


def create_user(validated_data: dict):
    """
    This method is used to take the user input and create a new user.
    Common for all users.
    """
    fields = [
        "username",
        "email",
        "password",
        "full_name",
        "street",
        "city",
        "state",
        "zip_code",
        "country",
        "user_type",
    ]

    for field in fields:
        if field not in validated_data:
            raise ValueError(f"{field} is required")

    user = User.objects.create(
        username=validated_data.pop("username"),
        email=validated_data.pop("email"),
        password=make_password(validated_data.pop("password")),
        full_name=validated_data.pop("full_name"),
        street=validated_data.pop("street"),
        state=validated_data.pop("state"),
        city=validated_data.pop("city"),
        zip_code=validated_data.pop("zip_code"),
        contact_no=validated_data.pop("contact_no"),
        user_type=validated_data.pop("user_type"),
    )

    # Extract language from request
    if "language" in validated_data:
        language = validated_data.pop("language")
        if isinstance(language, str):
            language = [language]
        UserLanguage.objects.bulk_create(
            [UserLanguage(user=user, language=lang) for lang in language]
        )

    return user
