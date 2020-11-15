from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase
from users.serializers import UserSerializer
from users.views import UserList

User = get_user_model()


class UserListViewTestCase(APITestCase):
    def test_GET_returns_a_list_of_users(self):
        user = User.objects.create(username='test', password='test@123')
        serializer = UserSerializer(user)
        request = APIRequestFactory().get('')
        response = UserList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(serializer.data, response.data)

    def test_successful_POST_creates_a_user(self):
        request = APIRequestFactory().post(
            '', {'username': 'test', 'password': 'test@123'})
        response = UserList.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='test')
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data, response.data)

    def test_invalid_data_returns_400(self):
        request = APIRequestFactory().post(
            '', {'username': '', 'password': ''})
        response = UserList.as_view()(request)
        self.assertEqual(response.status_code, 400)
