import uuid
from rest_framework.test import APITestCase
from users.factories import UserFactory
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

    def test_upvote(self):
        post = PostFactory()
        user = UserFactory()
        post.upvote(user)
        self.assertIn(user, post.upvoted_by.all())
        self.assertNotIn(user, post.downvoted_by.all())
        self.assertTrue(post.likes(user))
        self.assertEqual(post.ups, 1)
        self.assertEqual(post.downs, 0)

    def test_upvote_after_upvote(self):
        post = PostFactory()
        user = UserFactory()
        post.upvote(user)
        post.upvote(user)
        self.assertIn(user, post.upvoted_by.all())
        self.assertNotIn(user, post.downvoted_by.all())
        self.assertTrue(post.likes(user))
        self.assertEqual(post.ups, 1)
        self.assertEqual(post.downs, 0)

    def test_downvote(self):
        post = PostFactory()
        user = UserFactory()
        post.downvote(user)
        self.assertNotIn(user, post.upvoted_by.all())
        self.assertIn(user, post.downvoted_by.all())
        self.assertEqual(post.likes(user), False)
        self.assertEqual(post.ups, 0)
        self.assertEqual(post.downs, 1)

    def test_downvote_after_downvote(self):
        post = PostFactory()
        user = UserFactory()
        post.downvote(user)
        post.downvote(user)
        self.assertNotIn(user, post.upvoted_by.all())
        self.assertIn(user, post.downvoted_by.all())
        self.assertEqual(post.likes(user), False)
        self.assertEqual(post.ups, 0)
        self.assertEqual(post.downs, 1)

    def test_downvote_after_upvote(self):
        post = PostFactory()
        user = UserFactory()
        post.upvote(user)
        post.downvote(user)
        self.assertNotIn(user, post.upvoted_by.all())
        self.assertIn(user, post.downvoted_by.all())
        self.assertEqual(post.likes(user), False)
        self.assertEqual(post.ups, 0)
        self.assertEqual(post.downs, 1)

    def test_upvote_after_downvote(self):
        post = PostFactory()
        user = UserFactory()
        post.downvote(user)
        post.upvote(user)
        self.assertIn(user, post.upvoted_by.all())
        self.assertNotIn(user, post.downvoted_by.all())
        self.assertTrue(post.likes(user))
        self.assertEqual(post.ups, 1)
        self.assertEqual(post.downs, 0)

    def test_unvote_after_upvote(self):
        post = PostFactory()
        user = UserFactory()
        post.upvote(user)
        post.unvote(user)
        self.assertNotIn(user, post.upvoted_by.all())
        self.assertNotIn(user, post.downvoted_by.all())
        self.assertIsNone(post.likes(user))
        self.assertEqual(post.ups, 0)
        self.assertEqual(post.downs, 0)

    def test_unvote_after_downvote(self):
        post = PostFactory()
        user = UserFactory()
        post.downvote(user)
        post.unvote(user)
        self.assertNotIn(user, post.upvoted_by.all())
        self.assertNotIn(user, post.downvoted_by.all())
        self.assertIsNone(post.likes(user))
        self.assertEqual(post.ups, 0)
        self.assertEqual(post.downs, 0)

    def test_unvote_without_upvote_or_downvote(self):
        post = PostFactory()
        user = UserFactory()
        post.unvote(user)
        self.assertNotIn(user, post.upvoted_by.all())
        self.assertNotIn(user, post.downvoted_by.all())
        self.assertIsNone(post.likes(user))
        self.assertEqual(post.ups, 0)
        self.assertEqual(post.downs, 0)
