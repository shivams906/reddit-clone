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
        Subreddit, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    # likes = models.BooleanField(null=True)
    # ups = models.IntegerField(default=0)
    # downs = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    # def upvote(self):
    #     if self.likes == False:
    #         self.downs -= 1
    #     self.ups += 1
    #     self.likes = True
    #     self.save()

    # def downvote(self):
    #     if self.likes == True:
    #         self.ups -= 1
    #     self.downs += 1
    #     self.likes = False
    #     self.save()

    # def unvote(self):
    #     if self.likes == True:
    #         self.ups -= 1
    #     elif self.likes == False:
    #         self.downs -= 1
    #     self.likes = None
    #     self.save()
