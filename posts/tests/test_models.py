import uuid
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

    def test_id_is_instance_of_uuid(self):
        post = PostFactory()
        self.assertIsInstance(post.id, uuid.UUID)

    def test_can_upvote_post(self):
        post = PostFactory()
        post.upvote()
        post.refresh_from_db()
        self.assertTrue(post.likes)
        self.assertEqual(post.ups, 1)

    def test_can_downvote_post(self):
        post = PostFactory()
        post.downvote()
        post.refresh_from_db()
        self.assertFalse(post.likes)
        self.assertEqual(post.downs, 1)

    def test_downvote_after_upvote(self):
        post = PostFactory()
        post.upvote()
        post.refresh_from_db()
        self.assertTrue(post.likes)
        self.assertEqual(post.ups, 1)

        post.downvote()
        post.refresh_from_db()
        self.assertFalse(post.likes)
        self.assertEqual(post.downs, 1)
        self.assertEqual(post.ups, 0)

    def test_upvote_after_downvote(self):
        post = PostFactory()
        post.downvote()
        post.refresh_from_db()
        self.assertFalse(post.likes)
        self.assertEqual(post.downs, 1)

        post.upvote()
        post.refresh_from_db()
        self.assertTrue(post.likes)
        self.assertEqual(post.ups, 1)
        self.assertEqual(post.downs, 0)

    def test_can_unvote_after_upvote(self):
        post = PostFactory()
        post.upvote()
        post.unvote()

        self.assertEqual(post.likes, None)
        self.assertEqual(post.ups, 0)
        self.assertEqual(post.downs, 0)

    def test_can_unvote_after_downvote(self):
        post = PostFactory()
        post.downvote()
        post.unvote()

        self.assertEqual(post.likes, None)
        self.assertEqual(post.ups, 0)
        self.assertEqual(post.downs, 0)
