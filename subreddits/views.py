from rest_framework import generics, permissions
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
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Subreddit.objects.all()
    serializer_class = SubredditSerializer
