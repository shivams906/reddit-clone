from rest_framework.test import APIRequestFactory, APITestCase
from posts.factories import PostFactory
from posts.models import Post
from posts.serializers import PostCreateSerializer, PostUpdateSerializer
from posts.views import PostList, PostDetail, Upvote, Downvote, Unvote
from subreddits.factories import SubredditFactory
from users.factories import UserFactory


class PostListTestCase(APITestCase):
    def test_GET_returns_list_of_posts(self):
        post1 = PostFactory()
        post1_serializer = PostCreateSerializer(post1)
        post2 = PostFactory()
        post2_serializer = PostCreateSerializer(post2)

        request = APIRequestFactory().get("")
        response = PostList.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(post1_serializer.data, response.data)
        self.assertIn(post2_serializer.data, response.data)

    def test_valid_POST_creates_post_object(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        request = APIRequestFactory().post(
            "", data={"title": "post 1", "subreddit": subreddit.pk}
        )
        request.user = user
        response = PostList.as_view()(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)

    def test_only_authenticated_users_can_POST(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().post(
            "", data={"title": "post 1", "subreddit": subreddit.pk}
        )
        response = PostList.as_view()(request)

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )


class PostDetailTestCase(APITestCase):
    def test_GET_returns_a_particular_post(self):
        post = PostFactory()
        post_serializer = PostUpdateSerializer(post)
        request = APIRequestFactory().get("")
        response = PostDetail.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, post_serializer.data)

    def test_PATCH_works(self):
        post = PostFactory(title="post")
        request = APIRequestFactory().patch("", data={"title": "changed post"})
        request.user = post.author
        response = PostDetail.as_view()(request, pk=post.pk)
        post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.title, "changed post")

    def test_PUT_works(self):
        post = PostFactory(title="post")
        request = APIRequestFactory().put("", data={"title": "changed post"})
        request.user = post.author
        response = PostDetail.as_view()(request, pk=post.pk)
        post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.title, "changed post")

    def test_only_authenticated_users_can_PATCH(self):
        post = PostFactory()
        request = APIRequestFactory().patch("", data={"title": "changed post"})
        response = PostDetail.as_view()(request, pk=post.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_only_authenticated_users_can_PUT(self):
        post = PostFactory()
        request = APIRequestFactory().put("", data={"title": "changed post"})
        response = PostDetail.as_view()(request, pk=post.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_only_author_can_PATCH_to_their_post(self):
        post = PostFactory()
        request = APIRequestFactory().patch("", data={"title": "changed post"})
        second_user = UserFactory()
        request.user = second_user
        response = PostDetail.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 403)

    def test_only_author_can_PUT_to_their_post(self):
        post = PostFactory()
        request = APIRequestFactory().put("", data={"title": "changed post"})
        second_user = UserFactory()
        request.user = second_user
        response = PostDetail.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 403)

    def test_DELETE_works(self):
        post = PostFactory()
        request = APIRequestFactory().delete("")
        request.user = post.author
        response = PostDetail.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), 0)

    def test_only_authenticated_users_can_DELETE(self):
        post = PostFactory()
        request = APIRequestFactory().delete("")
        response = PostDetail.as_view()(request, pk=post.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_only_author_can_DELETE_to_their_post(self):
        post = PostFactory()
        request = APIRequestFactory().delete("")
        second_user = UserFactory()
        request.user = second_user
        response = PostDetail.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 403)


class UpvoteTestCase(APITestCase):
    def test_POST_upvotes_the_post(self):
        user = UserFactory()
        post = PostFactory()
        request = APIRequestFactory().post("")
        request.user = user
        response = Upvote.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["likes"])
        self.assertEqual(response.data["ups"], 1)

    def test_only_authenticated_users_can_upvote(self):
        post = PostFactory()
        request = APIRequestFactory().post("")
        response = Upvote.as_view()(request, pk=post.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )


class DownvoteTestCase(APITestCase):
    def test_POST_downvotes_the_post(self):
        user = UserFactory()
        post = PostFactory()
        request = APIRequestFactory().post("")
        request.user = user
        response = Downvote.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["likes"], False)
        self.assertEqual(response.data["downs"], 1)

    def test_only_authenticated_users_can_downvote(self):
        post = PostFactory()
        request = APIRequestFactory().post("")
        response = Downvote.as_view()(request, pk=post.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )


class UnvoteTestCase(APITestCase):
    def test_POST_unvotes_the_post(self):
        user = UserFactory()
        post = PostFactory()

        post.upvote(user)
        request = APIRequestFactory().post("")
        request.user = user
        response = Unvote.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data["likes"])
        self.assertEqual(response.data["ups"], 0)
        self.assertEqual(response.data["downs"], 0)

        post.refresh_from_db()
        post.downvote(user)
        request = APIRequestFactory().post("")
        request.user = user
        response = Unvote.as_view()(request, pk=post.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data["likes"])
        self.assertEqual(response.data["ups"], 0)
        self.assertEqual(response.data["downs"], 0)

    def test_only_authenticated_users_can_unvote(self):
        post = PostFactory()
        request = APIRequestFactory().post("")
        response = Unvote.as_view()(request, pk=post.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
