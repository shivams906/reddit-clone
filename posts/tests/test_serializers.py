from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from posts.models import Post
from posts.serializers import PostSerializer
from subreddits.factories import SubredditFactory
from users.factories import UserFactory


class PostSerializerTestCase(APITestCase):
    def test_author_can_not_be_edited_directly(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        serializer = PostSerializer(data={
            'title': 'a post',
            'subreddit': subreddit.pk,
            'author': user.pk
        })
        if serializer.is_valid():
            with self.assertRaises(IntegrityError):
                serializer.save()

    def test_author_is_saved_with_save_method(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        serializer = PostSerializer(data={
            'title': 'a post',
            'subreddit': subreddit.pk,
        })
        if serializer.is_valid():
            serializer.save(author=user)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, user)