from django.urls import path
from .views import PostList, PostDetail, Upvote, Downvote, Unvote

urlpatterns = [
    path("", PostList.as_view()),
    path("<uuid:pk>/", PostDetail.as_view()),
    path('<uuid:pk>/upvote/', Upvote.as_view()),
    path('<uuid:pk>/downvote/', Downvote.as_view()),
    path('<uuid:pk>/unvote/', Unvote.as_view()),
]