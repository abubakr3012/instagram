from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User, Profile, Follow
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    RegisterSerializer,
    FollowUserSerializer,
)
from .permissions import IsOwnerOrReadOnly

UserModel = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class TokenRefresh(TokenRefreshView):
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserSearchView(generics.ListAPIView):
    serializer_class = FollowUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()
        if not query:
            return Profile.objects.none()
        return Profile.objects.filter(
            Q(user__username__icontains=query)
            | Q(user__email__icontains=query)
        ).select_related('user')[:20]


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileByUsernameView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(
            Profile.objects.select_related('user'),
            user__username=self.kwargs['username'],
        )


class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(UserModel, pk=user_id)
        if target == request.user:
            return Response(
                {'detail': 'Нельзя подписаться на себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target,
        )
        if not created:
            follow.delete()
            self._update_counts(request.user, target)
            return Response({'detail': 'Отписались.', 'is_following': False})

        self._update_counts(request.user, target)
        return Response(
            {'detail': 'Подписались.', 'is_following': True},
            status=status.HTTP_201_CREATED,
        )

    def _update_counts(self, follower, following):
        follower_profile, _ = Profile.objects.get_or_create(user=follower)
        following_profile, _ = Profile.objects.get_or_create(user=following)
        follower_profile.following_cnt = Follow.objects.filter(follower=follower).count()
        following_profile.follower_cnt = Follow.objects.filter(following=following).count()
        follower_profile.save(update_fields=['following_cnt'])
        following_profile.save(update_fields=['follower_cnt'])


class FollowersListView(generics.ListAPIView):
    serializer_class = FollowUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['user_id'])
        return Profile.objects.filter(
            user__in=Follow.objects.filter(following=user).values('follower')
        ).select_related('user')


class FollowingListView(generics.ListAPIView):
    serializer_class = FollowUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['user_id'])
        return Profile.objects.filter(
            user__in=Follow.objects.filter(follower=user).values('following')
        ).select_related('user')
