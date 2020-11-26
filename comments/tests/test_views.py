from rest_framework.test import APIRequestFactory, APITestCase
from comments.factories import CommentFactory
from comments.models import Comment
from comments.serializers import CommentSerializer
from comments.views import CommentList, CommentDetail
from posts.factories import PostFactory
from users.factories import UserFactory


class CommentListTestCase(APITestCase):
    def test_GET_returns_list_of_comments(self):
        comment1 = CommentFactory()
        comment_serializer1 = CommentSerializer(comment1)
        comment2 = CommentFactory()
        comment_serializer2 = CommentSerializer(comment2)
        request = APIRequestFactory().get("")
        response = CommentList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(comment_serializer1.data, response.data)
        self.assertIn(comment_serializer2.data, response.data)

    def test_POST_creates_a_comment(self):
        user = UserFactory()
        post = PostFactory()
        request = APIRequestFactory().post("", data={"text": "test comment"})
        request.user = user
        response = CommentList.as_view()(request, post_pk=post.pk)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, "test comment")

    def test_only_authenticated_users_can_POST(self):
        post = PostFactory()
        request = APIRequestFactory().post("", data={"text": "test comment"})
        response = CommentList.as_view()(request, post_pk=post.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )


class CommentDetailTestCase(APITestCase):
    def test_GET_returns_a_comment(self):
        comment = CommentFactory()
        comment_serializer = CommentSerializer(comment)
        request = APIRequestFactory().get("")
        response = CommentDetail.as_view()(request, pk=comment.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(comment_serializer.data, response.data)

    def test_PUT_works(self):
        comment = CommentFactory()
        request = APIRequestFactory().put("", data={"text": "changed comment"})
        request.user = comment.author
        response = CommentDetail.as_view()(request, pk=comment.pk)
        comment.refresh_from_db()
        comment_serializer = CommentSerializer(comment)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.text, "changed comment")
        self.assertEqual(comment_serializer.data, response.data)

    def test_only_authenticated_users_can_PUT(self):
        comment = CommentFactory()
        request = APIRequestFactory().put("", data={"text": "changed comment"})
        response = CommentDetail.as_view()(request, pk=comment.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_only_comment_author_can_PUT(self):
        comment = CommentFactory()
        user = UserFactory()
        request = APIRequestFactory().put("", data={"text": "changed comment"})
        request.user = user
        response = CommentDetail.as_view()(request, pk=comment.pk)
        self.assertEqual(response.status_code, 403)

    def test_PATCH_works(self):
        comment = CommentFactory()
        request = APIRequestFactory().patch("", data={"text": "changed comment"})
        request.user = comment.author
        response = CommentDetail.as_view()(request, pk=comment.pk)
        comment.refresh_from_db()
        comment_serializer = CommentSerializer(comment)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.text, "changed comment")
        self.assertEqual(comment_serializer.data, response.data)

    def test_only_authenticated_users_can_PATCH(self):
        comment = CommentFactory()
        request = APIRequestFactory().patch("", data={"text": "changed comment"})
        response = CommentDetail.as_view()(request, pk=comment.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_only_comment_author_can_PATCH(self):
        comment = CommentFactory()
        user = UserFactory()
        request = APIRequestFactory().patch("", data={"text": "changed comment"})
        request.user = user
        response = CommentDetail.as_view()(request, pk=comment.pk)
        self.assertEqual(response.status_code, 403)

    def test_DELETE_works(self):
        comment = CommentFactory()
        request = APIRequestFactory().delete("")
        request.user = comment.author
        response = CommentDetail.as_view()(request, pk=comment.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), 0)

    def test_only_authenticated_users_can_DELETE(self):
        comment = CommentFactory()
        request = APIRequestFactory().delete("")
        response = CommentDetail.as_view()(request, pk=comment.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_only_comment_author_can_DELETE(self):
        comment = CommentFactory()
        user = UserFactory()
        request = APIRequestFactory().delete("")
        request.user = user
        response = CommentDetail.as_view()(request, pk=comment.pk)
        self.assertEqual(response.status_code, 403)
