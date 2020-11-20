import uuid
from django.contrib.auth import get_user_model
from django.db import models
from subreddits.models import Subreddit

User = get_user_model()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    subreddit = models.ForeignKey(
        Subreddit, on_delete=models.CASCADE, related_name="posts"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    upvoted_by = models.ManyToManyField(User, related_name="upvoted_posts")
    downvoted_by = models.ManyToManyField(User, related_name="downvoted_posts")
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def likes(self, user=None):
        if user is not None:
            if user in self.upvoted_by.all():
                return True
            if user in self.downvoted_by.all():
                return False
        return None

    def upvote(self, user=None):
        if user is not None:
            if user not in self.upvoted_by.all():
                if user in self.downvoted_by.all():
                    self.downvoted_by.remove(user)
                    self.downs -= 1
                self.upvoted_by.add(user)
                self.ups += 1
                self.save()

    def downvote(self, user=None):
        if user is not None:
            if user not in self.downvoted_by.all():
                if user in self.upvoted_by.all():
                    self.upvoted_by.remove(user)
                    self.ups -= 1
                self.downvoted_by.add(user)
                self.downs += 1
                self.save()

    def unvote(self, user=None):
        if user is not None:
            if user in self.upvoted_by.all():
                self.upvoted_by.remove(user)
                self.ups -= 1
                self.save()
            if user in self.downvoted_by.all():
                self.downvoted_by.remove(user)
                self.downs -= 1
                self.save()
