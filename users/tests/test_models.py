from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class UserModelTestCase(APITestCase):
    def test_valid_data_creates_user(self):
        User.objects.create(username='test', password='test@123')
        self.assertTrue(User.objects.count(), 1)
