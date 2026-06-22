from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    UserSearchView,
    ProfileListView,
    ProfileDetailView,
    ProfileMeView,
    ProfileByUsernameView,
    RegisterView,
    LoginView,
    TokenRefresh,
    FollowToggleView,
    FollowersListView,
    FollowingListView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefresh.as_view(), name='token-refresh'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/follow/', FollowToggleView.as_view(), name='follow-toggle'),
    path('users/<int:user_id>/followers/', FollowersListView.as_view(), name='followers'),
    path('users/<int:user_id>/following/', FollowingListView.as_view(), name='following'),
    path('profiles/', ProfileListView.as_view(), name='profiles'),
    path('profiles/me/', ProfileMeView.as_view(), name='profile-me'),
    path('profiles/username/<str:username>/', ProfileByUsernameView.as_view(), name='profile-by-username'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
]
