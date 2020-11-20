from django.db.utils import IntegrityError
from rest_framework.test import APIRequestFactory, APITestCase
from posts.factories import PostFactory
from posts.models import Post
from posts.serializers import PostSerializer
from subreddits.factories import SubredditFactory
from users.factories import UserFactory


class PostSerializerTestCase(APITestCase):
    def test_author_can_not_be_edited_directly(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        serializer = PostSerializer(data={"title": "a post", "author": user.pk})
        if serializer.is_valid():
            with self.assertRaises(IntegrityError):
                serializer.save(subreddit=subreddit)

    def test_subreddit_field_can_not_be_edited_directly(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        post_serializer = PostSerializer(
            data={"title": "a post", "subreddit": subreddit.pk}
        )
        if post_serializer.is_valid():
            with self.assertRaises(IntegrityError):
                post_serializer.save(author=user)

    def test_author_and_subreddit_is_saved_with_save_method(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        serializer = PostSerializer(data={"title": "a post"})
        if serializer.is_valid():
            serializer.save(author=user, subreddit=subreddit)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, user)
        self.assertEqual(Post.objects.first().subreddit, subreddit)

    def test_ups_can_not_be_edited_directly(self):
        post = PostFactory()
        post_serializer = PostSerializer(post, data={"ups": 1}, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()
        post.refresh_from_db()
        self.assertEqual(post.ups, 0)

    def test_downs_can_not_be_edited_directly(self):
        post = PostFactory()
        post_serializer = PostSerializer(post, data={"downs": 1}, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()
        post.refresh_from_db()
        self.assertEqual(post.downs, 0)

    def test_likes_is_serialized_correctly(self):
        post = PostFactory()
        user = UserFactory()
        post.upvote(user)
        request = APIRequestFactory().get("")
        request.user = user
        post_serializer = PostSerializer(post, context={"request": request})
        self.assertIn("likes", post_serializer.data)
        self.assertEqual(post.likes(user), post_serializer.data["likes"])
