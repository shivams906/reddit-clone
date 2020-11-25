import factory
from comments.models import Comment
from users.factories import UserFactory
from posts.factories import PostFactory


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = "test comment"
    author = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
