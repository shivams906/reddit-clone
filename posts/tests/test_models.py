from rest_framework.test import APITestCase
from posts.factories import PostFactory
from posts.models import Post


class PostModelTestCase(APITestCase):
    def test_valid_data_creates_post(self):
        PostFactory()
        self.assertEqual(Post.objects.count(), 1)

    def test_string_representation(self):
        post = PostFactory()
        self.assertEqual(str(post), post.title)
