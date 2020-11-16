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
