from rest_framework import generics, permissions
from comments.models import Comment
from comments.permissions import IsAuthorOrReadOnly
from comments.serializers import CommentCreateSerializer, CommentUpdateSerializer
from posts.models import Post


class CommentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
