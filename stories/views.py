from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Stories, Actualnost, Archive
from .serializers import StoriesSerializer, ActualnostSerializer, ArchiveSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedAndOwner


class StoriesViewSet(viewsets.ModelViewSet):
    serializer_class = StoriesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Stories.objects.filter(
            is_deleted=False,
            expires_at__gt=timezone.now(),
        ).select_related('user')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        story = self.get_object()
        story.likes_cnt += 1
        story.save(update_fields=['likes_cnt'])
        return Response({'likes_cnt': story.likes_cnt})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def view(self, request, pk=None):
        story = self.get_object()
        story.views_cnt += 1
        story.save(update_fields=['views_cnt'])
        return Response({'views_cnt': story.views_cnt})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedAndOwner])
    def soft_delete(self, request, pk=None):
        story = self.get_object()
        story.is_deleted = True
        story.save(update_fields=['is_deleted'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActualnostViewSet(viewsets.ModelViewSet):
    serializer_class = ActualnostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Actualnost.objects.filter(
            is_deleted=False,
        ).select_related('stories', 'stories__user')


class ArchiveViewSet(viewsets.ModelViewSet):
    serializer_class = ArchiveSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        return Archive.objects.filter(
            user=self.request.user,
        ).select_related('user', 'video', 'stories')