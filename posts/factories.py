import factory
from .models import Post
from subreddits.factories import SubredditFactory
from users.factories import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f'post{n}')
    subreddit = factory.SubFactory(SubredditFactory)
    author = factory.SubFactory(UserFactory)
