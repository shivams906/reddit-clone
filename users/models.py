import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    friends = models.ManyToManyField('self')
    karma = models.IntegerField(default=0)

    def add_friend(self, user=None):
        self.friends.add(user)
        return self

    def remove_friend(self, user=None):
        self.friends.remove(user)
        return self
