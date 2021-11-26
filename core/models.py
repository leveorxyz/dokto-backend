import uuid
from django.db import models

# Create your models here.
class CoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_hidden_fields(cls):
        return ["created_at", "updated_at", "is_deleted", "deleted_at"]

    def update_from_validated_data(self, validated_data: dict, *args, **kwargs):
        fields = [field.name for field in self._meta.fields]

        for field in fields:
            if field in validated_data:
                setattr(self, field, validated_data.pop(field))

        self.save()

    class Meta:
        abstract = True
