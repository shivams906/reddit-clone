from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from users.serializers import UserSerializer

User = get_user_model()


class UserSerializerTestCase(APITestCase):
    def test_can_not_view_password(self):
        user = User.objects.create(username='test', password='test@123')
        serializer = UserSerializer(user)
        self.assertNotIn('password', serializer.data)

    def test_can_not_edit_karma_directly(self):
        user = User.objects.create(username='test', password='test@123')
        serializer = UserSerializer(user, data={'karma': 10}, partial=True)
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(serializer.instance.karma, 0)

    def test_can_not_edit_friends_directly(self):
        user1 = User.objects.create(username='test1', password='test@123')
        user2 = User.objects.create(username='test2', password='test@123')
        serializer = UserSerializer(
            user1, data={'friends': [user2.pk, ]}, partial=True)
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(serializer.instance.friends.count(), 0)
