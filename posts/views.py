from rest_framework import generics, permissions
from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostCreateSerializer, PostUpdateSerializer


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
