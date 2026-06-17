from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Comment, Like
from .serializers import CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        video_id = self.kwargs["video_id"]
        return (
            Comment.objects
            .filter(video_id=video_id, parent_comment__isnull=True, is_deleted=False)
            .prefetch_related("replies__likes", "likes")
            .select_related("user")
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.select_related("user").prefetch_related("replies", "likes")

    def perform_destroy(self, instance):
        # Мягкое удаление вместо реального
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])


class CommentLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, is_deleted=False)
        like, created = Like.objects.get_or_create(
            user=request.user, comment=comment
        )
        if not created:
            like.delete()
            return Response(
                {"detail": "Лайк снят.", "likes_count": comment.likes.count()},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Лайк поставлен.", "likes_count": comment.likes.count()},
            status=status.HTTP_201_CREATED,
        )


class VideoLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        like, created = Like.objects.get_or_create(
            user=request.user, video_id=video_id
        )
        if not created:
            like.delete()
            return Response(
                {"detail": "Лайк снят."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Лайк поставлен."},
            status=status.HTTP_201_CREATED,
        )