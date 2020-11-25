from rest_framework.test import APITestCase
from comments.models import Comment
from comments.factories import CommentFactory


class CommentModelTestCase(APITestCase):
    def test_valid_data_creates_model(self):
        CommentFactory()
        self.assertEqual(Comment.objects.count(), 1)

    def test_string_representation(self):
        comment = CommentFactory()
        self.assertEqual(str(comment), comment.text)
