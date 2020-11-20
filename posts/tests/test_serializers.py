from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from posts.factories import PostFactory
from posts.models import Post
from posts.serializers import PostCreateSerializer, PostUpdateSerializer
from subreddits.factories import SubredditFactory
from users.factories import UserFactory


class PostSerializerTestCase(APITestCase):
    def test_author_can_not_be_edited_directly(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        serializer = PostCreateSerializer(
            data={"title": "a post", "subreddit": subreddit.pk, "author": user.pk}
        )
        if serializer.is_valid():
            with self.assertRaises(IntegrityError):
                serializer.save()

    def test_author_is_saved_with_save_method(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        serializer = PostCreateSerializer(
            data={
                "title": "a post",
                "subreddit": subreddit.pk,
            }
        )
        if serializer.is_valid():
            serializer.save(author=user)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, user)

    # def test_likes_can_not_be_edited_directly(self):
    #     post = PostFactory()
    #     post_serializer = PostCreateSerializer(post, data={"likes": True}, partial=True)
    #     if post_serializer.is_valid():
    #         post_serializer.save()
    #     post.refresh_from_db()
    #     self.assertEqual(post.likes, None)

    # def test_ups_can_not_be_edited_directly(self):
    #     post = PostFactory()
    #     post_serializer = PostCreateSerializer(post, data={"ups": 1}, partial=True)
    #     if post_serializer.is_valid():
    #         post_serializer.save()
    #     post.refresh_from_db()
    #     self.assertEqual(post.ups, 0)

    # def test_downs_can_not_be_edited_directly(self):
    #     post = PostFactory()
    #     post_serializer = PostCreateSerializer(post, data={"downs": 1}, partial=True)
    #     if post_serializer.is_valid():
    #         post_serializer.save()
    #     post.refresh_from_db()
    #     self.assertEqual(post.downs, 0)


class PostUpdateSerializerTestCase(APITestCase):
    def test_subreddit_field_can_not_be_updated(self):
        post = PostFactory()
        subreddit = SubredditFactory()
        post_serializer = PostUpdateSerializer(
            post, data={"subreddit": subreddit.pk}, partial=True
        )
        if post_serializer.is_valid():
            post_serializer.save()
        post.refresh_from_db()
        self.assertNotEqual(post.subreddit, subreddit.pk)
