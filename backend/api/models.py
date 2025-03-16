from django.db import models
from django.contrib.auth.models import User

class TextDocument(models.Model):
    content = models.TextField()
    processed = models.BooleanField(default=False)

class UserQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_text = models.TextField()
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
