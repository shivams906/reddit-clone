from django.urls import path
from rest_framework.authtoken import views
from .views import UserList, UserDetail

urlpatterns = [
    path("", UserList.as_view()),
    path("<uuid:pk>/", UserDetail.as_view()),
    path("get-auth-token/", views.obtain_auth_token),
]