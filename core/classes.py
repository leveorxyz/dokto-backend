import os
from typing import Optional
from datetime import datetime, timedelta, timezone

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class OverwriteFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name: str, max_length: Optional[int]):
        if self.exists(name):
            self.delete(name)
        return name


class FileManager:
    def __init__(self):
        self.storage_system = OverwriteFileSystemStorage()

    def save_file(self, file: any, *folder_path):
        file_path = os.path.join(settings.MEDIA_ROOT, *folder_path, file.name)
        self.storage_system.save(file_path, file)
        return file_path

    def delete_file(self, path: str):
        self.storage_system.delete(path)


class CustomTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def expires_in(self, token):
        time_elapsed = datetime.now(timezone.utc) - token.created
        return (
            timedelta(seconds=settings.USER_AUTH_TOKEN_EXPIRATION_SECONDS)
            - time_elapsed
        )

    def is_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.get(key=key)
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted.")

        if self.is_expired(token):
            token.delete()
            raise AuthenticationFailed("Token expired.")

        return (token.user, token)
