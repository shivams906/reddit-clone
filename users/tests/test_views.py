from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase
from users.factories import UserFactory
from users.serializers import UserSerializer
from users.views import UserList, UserDetail

User = get_user_model()


class UserListViewTestCase(APITestCase):
    def test_GET_returns_a_list_of_users(self):
        user = UserFactory()
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


class UserDetailViewTestCase(APITestCase):
    def test_GET_returns_a_particular_user(self):
        user = UserFactory()
        serializer = UserSerializer(user)
        request = APIRequestFactory().get('')
        response = UserDetail.as_view()(request, pk=user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer.data, response.data)

    def test_PUT_replaces_all_data(self):
        user = UserFactory()
        request = APIRequestFactory().put(
            '', {'username': 'test1', 'password': 'test@321'})
        request.user = user
        response = UserDetail.as_view()(request, pk=user.pk)
        changed_user = User.objects.get(pk=user.pk)
        serializer = UserSerializer(changed_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(changed_user.username, 'test1')
        self.assertEqual(changed_user.password, 'test@321')
        self.assertEqual(serializer.data, response.data)

    def test_PATCH_replaces_some_data(self):
        user = UserFactory()
        request = APIRequestFactory().patch(
            '', {'username': 'test1'})
        request.user = user
        response = UserDetail.as_view()(request, pk=user.pk)
        changed_user = User.objects.get(pk=user.pk)
        serializer = UserSerializer(changed_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(changed_user.username, 'test1')
        self.assertEqual(changed_user.password, 'test@123')
        self.assertEqual(serializer.data, response.data)

    def test_unauthenticated_users_can_not_PUT(self):
        user = UserFactory()
        request = APIRequestFactory().put(
            '', {'username': 'test1', 'password': 'test@321'})
        response = UserDetail.as_view()(request, pk=user.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_unauthenticated_users_can_not_PATCH(self):
        user = UserFactory()
        request = APIRequestFactory().patch(
            '', {'username': 'test1'})
        response = UserDetail.as_view()(request, pk=user.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_DELETE_deletes_the_user_object(self):
        user = UserFactory()
        request = APIRequestFactory().delete('')
        request.user = user
        response = UserDetail.as_view()(request, pk=user.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 0)

    def test_unauthenticated_users_can_not_DELETE(self):
        user = UserFactory()
        request = APIRequestFactory().delete('')
        response = UserDetail.as_view()(request, pk=user.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_user_can_PUT_to_own_data_only(self):
        user = UserFactory()
        user2 = UserFactory()
        request = APIRequestFactory().put(
            '', {'username': 'testuser2', 'password': 'test@321'})
        request.user = user
        response = UserDetail.as_view()(request, pk=user2.pk)
        self.assertEqual(response.status_code, 403)

    def test_user_can_PATCH_to_own_data_only(self):
        user = UserFactory()
        user2 = UserFactory()
        request = APIRequestFactory().patch(
            '', {'username': 'testuser2'})
        request.user = user
        response = UserDetail.as_view()(request, pk=user2.pk)
        self.assertEqual(response.status_code, 403)

    def test_user_can_DELETE_to_own_data_only(self):
        user = UserFactory()
        user2 = UserFactory()
        request = APIRequestFactory().delete('')
        request.user = user
        response = UserDetail.as_view()(request, pk=user2.pk)
        self.assertEqual(response.status_code, 403)
