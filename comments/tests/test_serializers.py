from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from comments.models import Comment
from comments.serializers import CommentSerializer
from posts.factories import PostFactory
from users.factories import UserFactory


class CommentSerializerTestCase(APITestCase):
    def test_author_can_not_be_edited_directly(self):
        user = UserFactory()
        post = PostFactory()
        comment_serializer = CommentSerializer(
            data={"text": "test comment", "author": user.pk}
        )
        if comment_serializer.is_valid():
            with self.assertRaises(IntegrityError):
                comment_serializer.save(post=post)

    def test_post_can_not_be_edited_directly(self):
        user = UserFactory()
        post = PostFactory()
        comment_serializer = CommentSerializer(
            data={"text": "test comment", "post": post.pk}
        )
        if comment_serializer.is_valid():
            with self.assertRaises(IntegrityError):
                comment_serializer.save(author=user)

    def test_author_and_post_are_saved_with_save_method(self):
        user = UserFactory()
        post = PostFactory()
        comment_serializer = CommentSerializer(data={"text": "test comment"})
        if comment_serializer.is_valid():
            comment_serializer.save(author=user, post=post)
            self.assertEqual(Comment.objects.count(), 1)
            self.assertEqual(Comment.objects.first().author, user)
            self.assertEqual(Comment.objects.first().post, post)
