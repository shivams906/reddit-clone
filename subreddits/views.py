from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Subreddit
from .permissions import IsOwnerOrReadOnly
from .serializers import SubredditSerializer


class SubredditList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Subreddit.objects.all()
    serializer_class = SubredditSerializer

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class SubredditDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Subreddit.objects.all()
    serializer_class = SubredditSerializer


class Subscribe(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        subreddit = get_object_or_404(Subreddit, pk=kwargs["pk"])
        subreddit.add_member(request.user)
        return Response()


class Unsubscribe(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        subreddit = get_object_or_404(Subreddit, pk=kwargs["pk"])
        subreddit.remove_member(request.user)
        return Response()
