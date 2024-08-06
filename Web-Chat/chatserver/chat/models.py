from django.db import models
from django.contrib.auth.models import User
import random
import uuid

def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, default=uuid.uuid4)
    users = models.ManyToManyField(User, through='RoomUser')

    def __str__(self):
        return self.name

class RoomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default=generate_random_color)

    class Meta:
        unique_together = ('user', 'chat_room')

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = generate_random_color()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} in {self.chat_room.name}'

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"
