from rest_framework import serializers
from comments.models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
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
        read_only_fields = ("author",)


class CommentUpdateSerializer(CommentCreateSerializer):
    class Meta(CommentCreateSerializer.Meta):
        read_only_fields = CommentCreateSerializer.Meta.read_only_fields + ("post",)
