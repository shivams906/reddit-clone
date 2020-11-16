from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from subreddits.models import Subreddit
from subreddits.serializers import SubredditSerializer

User = get_user_model()


class SubredditSerailizerTestCase(APITestCase):
    def test_members_can_not_be_edited_directly(self):
        user = User.objects.create(username='test', password='test@123')
        user2 = User.objects.create(username='test2', password='test@123')
        serializer = SubredditSerializer(
            data={'name': 'test', 'description': 'sub for testing', 'members': [user2.pk, ]})
        if serializer.is_valid():
            serializer.save(admin=user)
        self.assertEqual(Subreddit.objects.count(), 1)
        subreddit = Subreddit.objects.first()
        self.assertEqual(subreddit.members.count(), 0)
