from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.PrimaryKeyRelatedField(
        allow_empty=False, many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'karma', 'friends', 'subscriptions')
        read_only_fields = ('karma', 'friends', )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
