import factory
from .models import Subreddit
from users.factories import UserFactory


class SubredditFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subreddit

    name = factory.Sequence(lambda n: f'subreddit{n}')
    description = 'sub for testing'
    admin = factory.SubFactory(UserFactory)
