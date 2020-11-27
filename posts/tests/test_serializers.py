from django.db.utils import IntegrityError
from rest_framework.test import APIRequestFactory, APITestCase
from comments.factories import CommentFactory
from posts.factories import PostFactory
from posts.models import Post
from posts.serializers import PostCreateSerializer, PostUpdateSerializer
from subreddits.factories import SubredditFactory
from users.factories import UserFactory


class PostCreateSerializerTestCase(APITestCase):
    def test_author_can_not_be_edited_directly(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        serializer = PostCreateSerializer(
            data={"title": "a post", "author": user.pk, "subreddit": subreddit.pk}
        )
        if serializer.is_valid():
            with self.assertRaises(IntegrityError):
                serializer.save()

    def test_author_is_saved_with_save_method(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        serializer = PostCreateSerializer(
            data={"title": "a post", "subreddit": subreddit.pk}
        )
        if serializer.is_valid():
            serializer.save(author=user)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, user)
        self.assertEqual(Post.objects.first().subreddit, subreddit)

    def test_ups_can_not_be_edited_directly(self):
        post = PostFactory()
        post_serializer = PostCreateSerializer(post, data={"ups": 1}, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()
        post.refresh_from_db()
        self.assertEqual(post.ups, 0)

    def test_downs_can_not_be_edited_directly(self):
        post = PostFactory()
        post_serializer = PostCreateSerializer(post, data={"downs": 1}, partial=True)
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
        post_serializer = PostCreateSerializer(post, context={"request": request})
        self.assertIn("likes", post_serializer.data)
        self.assertEqual(post.likes(user), post_serializer.data["likes"])

    def test_comments_can_not_be_edited_directly(self):
        post = PostFactory()
        comment = CommentFactory()
        post_serializer = PostCreateSerializer(
            post, data={"comments": [comment.pk]}, partial=True
        )
        if post_serializer.is_valid():
            post_serializer.save()
        post.refresh_from_db()
        self.assertEqual(post.comments.count(), 0)


class PostUpdateSerializerTestCase(APITestCase):
    def test_subreddit_field_can_not_be_updated(self):
        subreddit = SubredditFactory()
        post = PostFactory()
        post_serializer = PostUpdateSerializer(
            post, data={"subreddit": subreddit.pk}, partial=True
        )
        if post_serializer.is_valid():
            post_serializer.save()
        post.refresh_from_db()
        self.assertEqual(Post.objects.count(), 1)
        self.assertNotEqual(post.subreddit, subreddit)
