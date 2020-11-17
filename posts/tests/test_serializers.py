from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from posts.models import Post
from posts.serializers import PostSerializer
from subreddits.models import Subreddit
User = get_user_model()


class PostSerializerTestCase(APITestCase):
    def test_author_can_not_be_edited_directly(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        serializer = PostSerializer(data={
            'title': 'a post',
            'subreddit': subreddit.pk,
            'author': user.pk
        })
        if serializer.is_valid():
            with self.assertRaises(IntegrityError):
                serializer.save()

    def test_author_is_saved_with_save_method(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        serializer = PostSerializer(data={
            'title': 'a post',
            'subreddit': subreddit.pk,
        })
        if serializer.is_valid():
            serializer.save(author=user)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, user)
