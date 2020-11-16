from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subreddit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return self.name

    def add_member(self, user=None):
        self.members.add(user)

    def remove_member(self, user=None):
        self.members.remove(user)
