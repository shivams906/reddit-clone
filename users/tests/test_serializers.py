from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from users.serializers import UserSerializer

User = get_user_model()


class UserSerializerTestCase(APITestCase):
    def test_can_not_view_password(self):
        user = User.objects.create(username='test', password='test@123')
        serializer = UserSerializer(user)
        self.assertNotIn('password', serializer.data)
