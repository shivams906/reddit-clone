from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from comments.factories import CommentFactory
from subreddits.factories import SubredditFactory
from users.factories import UserFactory
from users.serializers import UserSerializer

User = get_user_model()


class UserSerializerTestCase(APITestCase):
    def test_representation_of_data(self):
        user = UserFactory()
        serializer = UserSerializer(user)
        self.assertEqual(
            serializer.data,
            {
                "id": str(user.id),
                "username": user.username,
                "karma": user.karma,
                "comments": list(user.comments.all()),
                "posts": list(user.posts.all()),
                "friends": list(user.friends.all()),
                "subscriptions": list(user.subscriptions.all()),
            },
        )

    def test_subscriptions_can_not_be_edited_directly(self):
        subreddit = SubredditFactory()
        user = UserFactory()
        serializer = UserSerializer(
            instance=user,
            data={
                "subscriptions": [
                    subreddit.pk,
                ]
            },
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
        user.refresh_from_db()
        self.assertEqual(user.subscriptions.count(), 0)

    def test_can_not_view_password(self):
        user = UserFactory()
        serializer = UserSerializer(user)
        self.assertNotIn("password", serializer.data)

    def test_can_not_edit_karma_directly(self):
        user = UserFactory()
        serializer = UserSerializer(user, data={"karma": 10}, partial=True)
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(serializer.instance.karma, 0)

    def test_can_not_edit_friends_directly(self):
        user1 = UserFactory()
        user2 = UserFactory()
        serializer = UserSerializer(
            user1,
            data={
                "friends": [
                    user2.pk,
                ]
            },
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(serializer.instance.friends.count(), 0)

    def test_comments_can_not_be_edited_directly(self):
        user = UserFactory()
        comment = CommentFactory()
        serializer = UserSerializer(user, data={"comments": [comment.pk]}, partial=True)
        if serializer.is_valid():
            serializer.save()
        user.refresh_from_db()
        self.assertEqual(user.comments.count(), 0)
