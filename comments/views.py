from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from comments.models import Comment
from comments.permissions import IsAuthorOrReadOnly
from comments.serializers import CommentSerializer
from posts.models import Post


class CommentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        serializer.save(author=self.request.user, post=post)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
