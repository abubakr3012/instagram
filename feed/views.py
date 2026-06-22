from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from posts.models import Post
from posts.serializers import PostSerializer
from users.models import Follow


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            following_ids = Follow.objects.filter(
                follower=user
            ).values_list('following_id', flat=True)
            return Post.objects.filter(
                user_id__in=list(following_ids) + [user.id]
            ).select_related('user').prefetch_related('likes', 'comments')
        return Post.objects.select_related('user').prefetch_related(
            'likes', 'comments'
        )[:20]
