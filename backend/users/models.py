from django.db import models
from django.conf import settings

class FriendRequest(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_requests'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_requests'
    )
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("accepted", "Accepted")],
        default="pending"
    )
    createdAt = models.DateTimeField(auto_now_add=True)  # like timestamps
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} → {self.recipient} ({self.status})"
