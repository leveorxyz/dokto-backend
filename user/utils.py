import base64
from datetime import datetime, timezone

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
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
    profile_photo_data = validated_data.pop("profile_photo")
    file_name, file = generate_image_file_and_name(profile_photo_data, user.id)
    user.profile_photo.save(file_name, file, save=True)
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


def generate_image_file_and_name(image_data: str, user_id: int):
    """
    This method is used to generate a file name for the profile photo.
    """
    current_timestamp = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H_%M_%S")
    mimetype, data = image_data.split(";base64,")
    file_extention = mimetype.split("/")[-1]
    image_name = get_valid_filename(f"{user_id}_{current_timestamp}.{file_extention}")
    image_file = ContentFile(base64.b64decode(data), name=image_name)
    return image_name, image_file