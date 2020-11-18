from rest_framework import serializers
from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at',
                  'modified_at', 'subreddit', 'author',)
        read_only_fields = ('author',)


class PostUpdateSerializer(PostCreateSerializer):
    class Meta(PostCreateSerializer.Meta):
        read_only_fields = PostCreateSerializer.Meta.read_only_fields + \
            ('subreddit',)
