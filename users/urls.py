from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    ProfileListView,
    ProfileDetailView,
    RegisterView,
    LoginView
)

urlpatterns = [

    path(
        "users/",
        UserListView.as_view(),
        name="users"
    ),

    path(
        "users/<int:pk>/",
        UserDetailView.as_view(),
        name="user-detail"
    ),

    path(
        "profiles/",
        ProfileListView.as_view(),
        name="profiles"
    ),

    path(
        "profiles/<int:pk>/",
        ProfileDetailView.as_view(),
        name="profile-detail"
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),


    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),
]