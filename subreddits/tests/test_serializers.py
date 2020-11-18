from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from posts.factories import PostFactory
from subreddits.factories import SubredditFactory
from subreddits.models import Subreddit
from subreddits.serializers import SubredditSerializer
from users.factories import UserFactory

User = get_user_model()


class SubredditSerailizerTestCase(APITestCase):
    def test_members_can_not_be_edited_directly(self):
        user1 = UserFactory()
        user2 = UserFactory()
        serializer = SubredditSerializer(
            data={'name': 'test', 'description': 'sub for testing', 'members': [user2.pk, ]})
        if serializer.is_valid():
            serializer.save(admin=user1)
        self.assertEqual(Subreddit.objects.count(), 1)
        subreddit = Subreddit.objects.first()
        self.assertEqual(subreddit.members.count(), 0)

    def test_save_method_saves_admin_correctly(self):
        user = UserFactory()
        serializer = SubredditSerializer(
            data={'name': 'test', 'description': 'sub for testing'})
        if serializer.is_valid():
            serializer.save(admin=user)
        subreddit = Subreddit.objects.first()
        self.assertEqual(subreddit.admin, user)

    def test_posts_can_not_be_edited_directly(self):
        subreddit = SubredditFactory()
        post = PostFactory()
        subreddit_serializer = SubredditSerializer(
            subreddit, data={'posts': [post.pk, ]}, partial=True)
        if subreddit_serializer.is_valid():
            subreddit_serializer.save()
        subreddit.refresh_from_db()
        self.assertEqual(subreddit.posts.count(), 0)
