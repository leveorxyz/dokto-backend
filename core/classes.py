from typing import Optional
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from rest_framework.authentication import TokenAuthentication


class OverwriteFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name: str, max_length: Optional[int]):
        if self.exists(name):
            self.delete(name)
        return name


class FileManager:
    def __init__(self):
        self.storage_system = OverwriteFileSystemStorage()

    def delete_file(self, path: str):
        self.storage_system.delete(path)


class CustomTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"
