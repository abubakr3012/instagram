from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostSerializer, PostMusicSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related("user").all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    @action(
        detail=True,               
        methods=("patch",),
        url_path="add_music",
        serializer_class=PostMusicSerializer,
    )
    def add_music(self, request, pk=None):
        post = self.get_object()   

        serializer = PostMusicSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(PostSerializer(post, context={"request": request}).data)

    @action(
        detail=True,               
        methods=("delete",),
        url_path="remove_music",
    )
    def remove_music(self, request, pk=None):
        post = self.get_object()

        if not post.music:
            return Response(
                {"detail": "У этого поста нет музыки."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.music.delete(save=True)   
        return Response(
            {"detail": "Музыка удалена."},
            status=status.HTTP_200_OK,
        )