import uuid
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from subreddits.factories import SubredditFactory
from subreddits.models import Subreddit
from users.factories import UserFactory

User = get_user_model()


class SubredditModelTestCase(APITestCase):
    def test_valid_data_creates_subreddt(self):
        SubredditFactory()
        self.assertEqual(Subreddit.objects.count(), 1)

    def test_members_can_be_added(self):
        subreddit = SubredditFactory()
        user = UserFactory()
        subreddit.add_member(user)
        self.assertIn(user, subreddit.members.all())

    def test_members_can_be_removed(self):
        subreddit = SubredditFactory()
        user = UserFactory()
        subreddit.add_member(user)
        self.assertIn(user, subreddit.members.all())

        subreddit.remove_member(user)
        self.assertNotIn(user, subreddit.members.all())

    def test_string_representation(self):
        subreddit = SubredditFactory()
        self.assertEqual(str(subreddit), subreddit.name)

    def test_uuid_is_saved_as_id(self):
        subreddit = SubredditFactory()
        self.assertIsInstance(subreddit.id, uuid.UUID)
