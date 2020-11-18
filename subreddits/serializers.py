from rest_framework import serializers
from .models import Subreddit


class SubredditSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(
        allow_empty=False, many=True, read_only=True)

    class Meta:
        model = Subreddit
        fields = ('id', 'name', 'description',
                  'created_at', 'modified_at', 'members', 'posts')
        read_only_fields = ('members',)
