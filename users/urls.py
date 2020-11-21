from django.urls import path
from .views import UserList, UserDetail

urlpatterns = [
    path("", UserList.as_view()),
    path("<uuid:pk>/", UserDetail.as_view()),
]