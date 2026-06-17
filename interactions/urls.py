from django.urls import path
from . import views

urlpatterns = [
    path(
        "videos/<int:video_id>/comments/",
        views.CommentListCreateView.as_view(),
        name="comment-list-create",
    ),
    path(
        "comments/<int:pk>/",
        views.CommentDetailView.as_view(),
        name="comment-detail",
    ),
    path(
        "comments/<int:pk>/like/",
        views.CommentLikeToggleView.as_view(),
    ),
    path(
        "videos/<int:video_id>/like/",
        views.VideoLikeToggleView.as_view(),
        name="video-like-toggle",
    ),
]