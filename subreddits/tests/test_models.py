import uuid
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from subreddits.models import Subreddit

User = get_user_model()


class SubredditModelTestCase(APITestCase):
    def test_valid_data_creates_subreddt(self):
        user = User.objects.create(username='test', password='test@123')
        Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        self.assertEqual(Subreddit.objects.count(), 1)

    def test_members_can_be_added(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        user2 = User.objects.create(username='test2', password='test@123')
        subreddit.add_member(user2)
        self.assertIn(user2, subreddit.members.all())

    def test_members_can_be_removed(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        user2 = User.objects.create(username='test2', password='test@123')
        subreddit.add_member(user2)
        self.assertIn(user2, subreddit.members.all())

        subreddit.remove_member(user2)
        self.assertNotIn(user2, subreddit.members.all())

    def test_string_representation(self):
        user = User.objects.create(username='test', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        self.assertEqual(str(subreddit), 'test')

    def test_uuid_is_saved_as_id(self):
        user = User.objects.create(username='test1', password='test@123')
        subreddit = Subreddit.objects.create(
            name='test', description='sub for testing', admin=user)
        self.assertIsInstance(subreddit.id, uuid.UUID)
