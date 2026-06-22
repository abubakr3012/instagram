from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Post, PostLike, PostComment
from .serializers import PostSerializer, PostMusicSerializer, PostCommentSerializer
from .permissions import IsAuthenticatedForWrite


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('user').prefetch_related('likes', 'comments')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedForWrite]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_comments'] = self.action == 'retrieve'
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        search = self.request.query_params.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(caption__icontains=search)
                | Q(user__username__icontains=search)
            )
        return queryset

    @action(detail=True, methods=['patch'], url_path='add_music', serializer_class=PostMusicSerializer)
    def add_music(self, request, pk=None):
        post = self.get_object()
        serializer = PostMusicSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(PostSerializer(post, context={'request': request}).data)

    @action(detail=True, methods=['delete'], url_path='remove_music')
    def remove_music(self, request, pk=None):
        post = self.get_object()
        if not post.music:
            return Response(
                {'detail': 'У этого поста нет музыки.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post.music.delete(save=True)
        return Response({'detail': 'Музыка удалена.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({
                'detail': 'Лайк снят.',
                'is_liked': False,
                'likes_count': post.likes.count(),
            })
        return Response({
            'detail': 'Лайк поставлен.',
            'is_liked': True,
            'likes_count': post.likes.count(),
        }, status=status.HTTP_201_CREATED)


class PostCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = PostCommentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return PostComment.objects.filter(
            post_id=self.kwargs['post_id'],
            is_deleted=False,
        ).select_related('user')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(user=self.request.user, post=post)


class PostCommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        comment = get_object_or_404(PostComment, pk=pk, user=request.user)
        comment.is_deleted = True
        comment.save(update_fields=['is_deleted'])
        return Response(status=status.HTTP_204_NO_CONTENT)
