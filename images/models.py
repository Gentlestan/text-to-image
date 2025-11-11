
# images/models.py
from django.db import models
from django.contrib.auth.models import User

class GeneratedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    image_url = models.URLField(default="https://example.com/placeholder.png")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prompt[:20]}"



