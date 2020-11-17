from rest_framework.test import APIRequestFactory, APITestCase
from posts.factories import PostFactory
from posts.serializers import PostSerializer
from posts.views import PostList


class PostListTestCase(APITestCase):
    def test_GET_returns_list_of_posts(self):
        post1 = PostFactory()
        post1_serializer = PostSerializer(post1)
        post2 = PostFactory()
        post2_serializer = PostSerializer(post2)

        request = APIRequestFactory().get('')
        response = PostList.as_view()(request)

        self.assertEqual(len(response.data), 2)
        self.assertIn(post1_serializer.data, response.data)
        self.assertIn(post2_serializer.data, response.data)
