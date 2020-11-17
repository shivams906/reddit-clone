from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from posts.models import Post
from subreddits.models import Subreddit

User = get_user_model()


class PostModelTestCase(APITestCase):
    def test_valid_data_creates_post(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        Post.objects.create(title='a post', subreddit=subreddit, author=user)
        self.assertEqual(Post.objects.count(), 1)

    def test_string_representation(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        post = Post.objects.create(
            title='a post', subreddit=subreddit, author=user)
        self.assertEqual(str(post), post.title)
