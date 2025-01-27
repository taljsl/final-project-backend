from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    # Represents a chat room
    name = models.CharField(max_length=100, unique=True)  # Room names must be unique

    def __str__(self):
        return self.name


class Message(models.Model):
    # Represents a message in a chat room
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically adds time

    def __str__(self):
        return f"[{self.timestamp}] {self.user}: {self.content}"
