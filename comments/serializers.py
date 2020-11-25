from rest_framework import serializers
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "created_at",
            "modified_at",
            "author",
            "post",
        )
        read_only_fields = (
            "author",
            "post",
        )
