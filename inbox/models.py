from django.db import models

from core.models import CoreModel
from user.models import User

# Create your models here.


class InboxChannel(CoreModel):
    first_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="first_user"
    )
    second_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="second_user"
    )


class InboxMessage(CoreModel):
    channel = models.ForeignKey(
        InboxChannel, on_delete=models.CASCADE, related_name="channel"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    message = models.TextField(max_length=512, blank=True, null=True, default=None)
    subject = models.CharField(blank=True, null=True, max_length=128, default=None)
    read_status = models.BooleanField(default=False)
