from django.urls import path
from .views import SubredditList, SubredditDetail, Subscribe

urlpatterns = [
    path("", SubredditList.as_view()),
    path("<uuid:pk>/", SubredditDetail.as_view()),
    path("<uuid:pk>/subscribe/", Subscribe.as_view()),
]