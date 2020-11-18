from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase
from subreddits.factories import SubredditFactory
from subreddits.models import Subreddit
from subreddits.serializers import SubredditSerializer
from subreddits.views import SubredditList, SubredditDetail, Subscribe
from users.factories import UserFactory

User = get_user_model()


class SubredditListTestCase(APITestCase):
    def test_GET_returns_list_of_subreddits(self):
        subreddit1 = SubredditFactory()
        serializer1 = SubredditSerializer(subreddit1)
        subreddit2 = SubredditFactory()
        serializer2 = SubredditSerializer(subreddit2)

        request = APIRequestFactory().get('')
        response = SubredditList.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)

    def test_valid_POST_creates_subreddit(self):
        user = UserFactory()
        request = APIRequestFactory().post(
            '', {'name': 'test', 'description': 'sub for testing'})
        request.user = user
        response = SubredditList.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subreddit.objects.count(), 1)

    def test_invalid_POST_returns_400(self):
        user = UserFactory()
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
        subreddit = SubredditFactory()
        serializer = SubredditSerializer(subreddit)
        request = APIRequestFactory().get('')
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer.data, response.data)

    def test_PUT_replaces_all_data(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().put(
            '', {'name': 'testing', 'description': 'subreddit for testing'})
        request.user = subreddit.admin
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        changed_subreddit = Subreddit.objects.get(pk=subreddit.pk)
        serializer = SubredditSerializer(changed_subreddit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(changed_subreddit.name, 'testing')
        self.assertEqual(changed_subreddit.description,
                         'subreddit for testing')
        self.assertEqual(serializer.data, response.data)

    def test_PATCH_replaces_some_data(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().patch(
            '', {'name': 'testing'})
        request.user = subreddit.admin
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        changed_subreddit = Subreddit.objects.get(pk=subreddit.pk)
        serializer = SubredditSerializer(changed_subreddit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(changed_subreddit.name, 'testing')
        self.assertEqual(changed_subreddit.description,
                         'sub for testing')
        self.assertEqual(serializer.data, response.data)

    def test_unauthenticated_users_can_not_PUT(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().put(
            '', {'name': 'testing', 'description': 'subreddit for testing'})
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_unauthenticated_users_can_not_PATCH(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().patch(
            '', {'name': 'testing'})
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_DELETE_deletes_the_user_object(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().delete('')
        request.user = subreddit.admin
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Subreddit.objects.count(), 0)

    def test_unauthenticated_users_can_not_DELETE(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().delete('')
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_user_can_PUT_to_own_data_only(self):
        subreddit = SubredditFactory()
        user = UserFactory()
        request = APIRequestFactory().put(
            '', {'name': 'testing', 'description': 'subreddit for testing'})
        request.user = user
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 403)

    def test_user_can_PATCH_to_own_data_only(self):
        subreddit = SubredditFactory()
        user = UserFactory()
        request = APIRequestFactory().patch(
            '', {'name': 'testing'})
        request.user = user
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 403)

    def test_user_can_DELETE_to_own_data_only(self):
        subreddit = SubredditFactory()
        user = UserFactory()
        request = APIRequestFactory().delete('')
        request.user = user
        response = SubredditDetail.as_view()(request, pk=subreddit.pk)
        self.assertEqual(response.status_code, 403)


class SubscribeTestCase(APITestCase):
    def test_authenticated_users_can_subscribe_to_a_subreddit(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().post('')
        user = UserFactory()
        request.user = user
        response = Subscribe.as_view()(request, pk=subreddit.pk)
        subreddit.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertIn(user, subreddit.members.all())

    def test_only_authenticated_users_can_subscribe(self):
        subreddit = SubredditFactory()
        request = APIRequestFactory().post('')
        response = Subscribe.as_view()(request, pk=subreddit.pk)
        subreddit.refresh_from_db()
        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(subreddit.members.count(), 0)
