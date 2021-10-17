import base64
from datetime import datetime, timezone

from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import get_valid_filename

from .models import User, UserLanguage


def create_user(validated_data: dict, user_type: str):
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
        "profile_photo",
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
        user_type=user_type,
    )

    # Extracting and saving the profile photo
    profile_photo: InMemoryUploadedFile = validated_data.pop("profile_photo")
    file_name = generate_image_file_name(
        profile_photo.content_type.split("/")[-1], user.id
    )
    user.profile_photo.save(file_name, profile_photo, save=True)
    user.save()

    # Extract language from request
    if "language" in validated_data:
        language = validated_data.pop("language")
        if isinstance(language, str):
            language = [language]
        UserLanguage.objects.bulk_create(
            [UserLanguage(user=user, language=lang) for lang in language]
        )

    return user


def generate_image_file_name(file_extention: str, user_id: int):
    """
    This method is used to generate a file name for the profile photo.
    """
    current_timestamp = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H_%M_%S")
    image_name = get_valid_filename(f"{user_id}_{current_timestamp}.{file_extention}")
    return image_name
