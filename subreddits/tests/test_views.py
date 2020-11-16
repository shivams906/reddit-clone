from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase
from subreddits.models import Subreddit
from subreddits.serializers import SubredditSerializer
from subreddits.views import SubredditList, SubredditDetail

User = get_user_model()


class SubredditListTestCase(APITestCase):
    def test_GET_returns_list_of_subreddits(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit1 = Subreddit.objects.create(
            name='test1', description='sub for testing', admin=user)
        serializer1 = SubredditSerializer(subreddit1)
        subreddit2 = Subreddit.objects.create(
            name='test2', description='sub for testing', admin=user)
        serializer2 = SubredditSerializer(subreddit2)

        request = APIRequestFactory().get('')
        response = SubredditList.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)

    def test_valid_POST_creates_subreddit(self):
        user = User.objects.create(username='test', password='test@123')
        request = APIRequestFactory().post(
            '', {'name': 'test', 'description': 'sub for testing'})
        request.user = user
        response = SubredditList.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subreddit.objects.count(), 1)

    def test_invalid_POST_returns_400(self):
        user = User.objects.create(username='test', password='test@123')
        request = APIRequestFactory().post('', {'name': '', 'description': ''})
        request.user = user
        response = SubredditList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Subreddit.objects.count(), 0)

    def test_only_authenticated_users_can_POST(self):
        request = APIRequestFactory().post(
            '', {'name': 'test', 'description': 'sub for testing'})
        response = SubredditList.as_view()(request)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')


class SubredditDetailTestCase(APITestCase):
    def test_GET_returns_a_particular_subreddit(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        serializer = SubredditSerializer(subreddit)
        request = APIRequestFactory().get('')
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer.data, response.data)

    def test_PUT_replaces_all_data(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        request = APIRequestFactory().put(
            '', {'name': 'testing', 'description': 'subreddit for testing'})
        request.user = user
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        changed_subreddit = Subreddit.objects.get(pk=subreddit.pk)
        serializer = SubredditSerializer(changed_subreddit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(changed_subreddit.name, 'testing')
        self.assertEqual(changed_subreddit.description,
                         'subreddit for testing')
        self.assertEqual(serializer.data, response.data)

    def test_PATCH_replaces_some_data(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        request = APIRequestFactory().patch(
            '', {'name': 'testing'})
        request.user = user
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        changed_subreddit = Subreddit.objects.get(pk=subreddit.pk)
        serializer = SubredditSerializer(changed_subreddit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(changed_subreddit.name, 'testing')
        self.assertEqual(changed_subreddit.description,
                         'sub for testing')
        self.assertEqual(serializer.data, response.data)

    def test_unauthenticated_users_can_not_PUT(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        request = APIRequestFactory().put(
            '', {'name': 'testing', 'description': 'subreddit for testing'})
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_unauthenticated_users_can_not_PATCH(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        request = APIRequestFactory().patch(
            '', {'name': 'testing'})
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_DELETE_deletes_the_user_object(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        request = APIRequestFactory().delete('')
        request.user = user
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Subreddit.objects.count(), 0)

    def test_unauthenticated_users_can_not_DELETE(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        request = APIRequestFactory().delete('')
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_user_can_PUT_to_own_data_only(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        user2 = User.objects.create(username='test2', password='test@123')
        request = APIRequestFactory().put(
            '', {'name': 'testing', 'description': 'subreddit for testing'})
        request.user = user2
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 403)

    def test_user_can_PATCH_to_own_data_only(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        user2 = User.objects.create(username='test2', password='test@123')
        request = APIRequestFactory().patch(
            '', {'name': 'testing'})
        request.user = user2
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 403)

    def test_user_can_DELETE_to_own_data_only(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        user2 = User.objects.create(username='test2', password='test@123')
        request = APIRequestFactory().delete('')
        request.user = user2
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 403)
