from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from subreddits.models import Subreddit
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer


class Upvote(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        post.upvote(request.user)
        post_serializer = PostUpdateSerializer(post, context={"request": request})
        return Response(post_serializer.data)


class Downvote(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        post.downvote(request.user)
        post_serializer = PostUpdateSerializer(post, context={"request": request})
        return Response(post_serializer.data)


class Unvote(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        post.unvote(request.user)
        post_serializer = PostUpdateSerializer(post, context={"request": request})
        return Response(post_serializer.data)
