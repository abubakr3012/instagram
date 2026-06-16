from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from .models import User, Profile
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    RegisterSerializer
)
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)



class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    permission_classes = [
        AllowAny
    ]



class LoginView(TokenObtainPairView):

    permission_classes = [
        AllowAny
    ]

class UserListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [
        AllowAny
    ]



class UserDetailView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [
        AllowAny
    ]


class ProfileListView(generics.ListAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [
        AllowAny
    ]



class ProfileDetailView(
    generics.RetrieveUpdateAPIView
):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


    permission_classes = [
        IsOwnerOrReadOnly
    ]