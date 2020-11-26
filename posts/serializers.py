from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "created_at",
            "modified_at",
            "subreddit",
            "author",
            "likes",
            "ups",
            "downs",
            "comments",
        )
        read_only_fields = (
            "subreddit",
            "author",
            "ups",
            "downs",
            "comments",
        )

    def get_likes(self, obj):
        if "request" in self.context:
            return obj.likes(self.context["request"].user)
