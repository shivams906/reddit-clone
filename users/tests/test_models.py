from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class UserModelTestCase(APITestCase):
    def test_valid_data_creates_user(self):
        User.objects.create(username='test', password='test@123')
        self.assertTrue(User.objects.count(), 1)

    def test_string_representaion(self):
        user = User.objects.create(username='test', password='test@123')
        self.assertEqual(str(user), 'test')

    def test_can_befriend_another_user(self):
        user1 = User.objects.create(username='test1', password='test@123')
        user2 = User.objects.create(username='test2', password='test@123')
        user1.add_friend(user2)
        self.assertIn(user2, user1.friends.all())
