from django.db import models
from loginApp.models import User



class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name='messages_to', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='messages_from', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
