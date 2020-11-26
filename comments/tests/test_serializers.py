from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from comments.factories import CommentFactory
from comments.models import Comment
from comments.serializers import CommentCreateSerializer, CommentUpdateSerializer
from posts.factories import PostFactory
from users.factories import UserFactory


class CommentCreateSerializerTestCase(APITestCase):
    def test_author_can_not_be_edited_directly(self):
        user = UserFactory()
        post = PostFactory()
        comment_serializer = CommentCreateSerializer(
            data={"text": "test comment", "author": user.pk, "post": post.pk}
        )
        if comment_serializer.is_valid():
            with self.assertRaises(IntegrityError):
                comment_serializer.save()

    def test_author_is_saved_with_save_method(self):
        user = UserFactory()
        post = PostFactory()
        comment_serializer = CommentCreateSerializer(
            data={"text": "test comment", "post": post.pk}
        )
        if comment_serializer.is_valid():
            comment_serializer.save(author=user)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, user)


class CommentUpdateSerializerTestCase(APITestCase):
    def test_post_can_not_be_updated(self):
        post = PostFactory()
        comment = CommentFactory()
        comment_serializer = CommentUpdateSerializer(
            comment, data={"post": post.pk}, partial=True
        )
        if comment_serializer.is_valid():
            comment_serializer.save()
        comment.refresh_from_db()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertNotEqual(comment.post, post)
