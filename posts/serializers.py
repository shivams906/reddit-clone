from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at',
                  'modified_at', 'subreddit', 'author',)
        read_only_fields = ('author',)


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at',
                  'modified_at', 'subreddit', 'author',)
        read_only_fields = ('author', 'subreddit')
