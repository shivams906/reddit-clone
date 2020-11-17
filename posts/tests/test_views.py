from rest_framework.test import APIRequestFactory, APITestCase
from posts.factories import PostFactory
from posts.models import Post
from posts.serializers import PostSerializer
from posts.views import PostList
from subreddits.factories import SubredditFactory
from users.factories import UserFactory


class PostListTestCase(APITestCase):
    def test_GET_returns_list_of_posts(self):
        post1 = PostFactory()
        post1_serializer = PostSerializer(post1)
        post2 = PostFactory()
        post2_serializer = PostSerializer(post2)

        request = APIRequestFactory().get('')
        response = PostList.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(post1_serializer.data, response.data)
        self.assertIn(post2_serializer.data, response.data)

    def test_valid_POST_creates_post_object(self):
        user = UserFactory()
        subreddit = SubredditFactory()
        request = APIRequestFactory().post(
            '', data={'title': 'post 1', 'subreddit': subreddit.pk})
        request.user = user
        response = PostList.as_view()(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)

    def test_only_authenticated_users_can_POST(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().post(
            '', data={'title': 'post 1', 'subreddit': subreddit.pk})
        response = PostList.as_view()(request)

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')
