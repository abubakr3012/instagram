from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Videos, Reposts, SavedVideos
from .serializers import (
    VideoSerializer, VideoCreateSerializer,
    RepostSerializer, SavedVideoSerializer
)
from .permissions import IsOwnerOrReadOnly, IsOwner


class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Videos.objects.filter(is_deleted=False).order_by('-created_at')


class VideoCreateView(generics.CreateAPIView):
    serializer_class = VideoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoDetailView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        video = get_object_or_404(Videos, pk=self.kwargs['pk'], is_deleted=False)
        Videos.objects.filter(pk=video.pk).update(views_cnt=video.views_cnt + 1)
        video.refresh_from_db()
        return video


class VideoDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Videos.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class MyVideosView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Videos.objects.filter(
            user=self.request.user, 
            is_deleted=False
        ).order_by('-created_at')



class RepostCreateView(generics.CreateAPIView):
    serializer_class = RepostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RepostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        repost = get_object_or_404(
            Reposts, pk=pk, user=request.user, is_deleted=False
        )
        repost.is_deleted = True
        repost.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyRepostsView(generics.ListAPIView):
    serializer_class = RepostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reposts.objects.filter(
            user=self.request.user, 
            is_deleted=False
        ).select_related('video')



class SaveVideoView(generics.CreateAPIView):
    serializer_class = SavedVideoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UnsaveVideoView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        saved = get_object_or_404(
            SavedVideos, pk=pk, user=request.user, is_deleted=False
        )
        saved.is_deleted = True
        saved.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MySavedVideosView(generics.ListAPIView):
    serializer_class = SavedVideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedVideos.objects.filter(
            user=self.request.user, 
            is_deleted=False
        ).select_related('video')