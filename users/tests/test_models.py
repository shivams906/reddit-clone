import uuid
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from users.factories import UserFactory

User = get_user_model()


class UserModelTestCase(APITestCase):
    def test_valid_data_creates_user(self):
        user = UserFactory()
        self.assertTrue(User.objects.count(), 1)

    def test_string_representaion(self):
        user = UserFactory()
        self.assertEqual(str(user), user.username)

    def test_can_befriend_another_user(self):
        user1 = UserFactory()
        user2 = UserFactory()

        user1.add_friend(user2)
        self.assertIn(user2, user1.friends.all())

    def test_can_remove_friend(self):
        user1 = UserFactory()
        user2 = UserFactory()

        user1.add_friend(user2)
        self.assertIn(user2, user1.friends.all())

        user1.remove_friend(user2)
        self.assertEqual(user1.friends.count(), 0)

    def test_uuid_is_saved_as_id(self):
        user = UserFactory()
        self.assertIsInstance(user.id, uuid.UUID)
