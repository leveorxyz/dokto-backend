from django.db import models
from django.db.models import Q

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
    encounter_reason = models.CharField(
        max_length=255, null=True, blank=True, default=""
    )

    def get_unread_msg_count(self, user: User) -> int:
        return self.message.filter(~Q(sender=user) & Q(read_status=False)).count()

    def __str__(self) -> str:
        return f"{self.id}"

    def __repr__(self) -> str:
        return self.__str__()


class InboxMessage(CoreModel):
    channel = models.ForeignKey(
        InboxChannel, on_delete=models.CASCADE, related_name="message"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    message = models.TextField(max_length=512, blank=True, null=True, default=None)
    subject = models.CharField(blank=True, null=True, max_length=128, default=None)
    read_status = models.BooleanField(default=False)
