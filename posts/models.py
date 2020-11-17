from django.contrib.auth import get_user_model
from django.db import models
from subreddits.models import Subreddit

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    subreddit = models.ForeignKey(
        Subreddit, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title
