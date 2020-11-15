from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    friends = models.ManyToManyField('self')

    def add_friend(self, user=None):
        self.friends.add(user)
        return self
