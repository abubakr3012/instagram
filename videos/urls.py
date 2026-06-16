from django.urls import path
from . import views

urlpatterns = [
    path('', views.VideoListView.as_view(), name='video-list'),
    path('create/', views.VideoCreateView.as_view(), name='video-create'),
    path('<int:pk>/', views.VideoDetailView.as_view(), name='video-detail'),
    path('<int:pk>/delete/', views.VideoDeleteView.as_view(), name='video-delete'),
    path('my/', views.MyVideosView.as_view(), name='my-videos'),

    path('reposts/create/', views.RepostCreateView.as_view(), name='repost-create'),
    path('reposts/<int:pk>/delete/', views.RepostDeleteView.as_view(), name='repost-delete'),
    path('reposts/my/', views.MyRepostsView.as_view(), name='my-reposts'),

    path('saved/save/', views.SaveVideoView.as_view(), name='save-video'),
    path('saved/<int:pk>/unsave/', views.UnsaveVideoView.as_view(), name='unsave-video'),
    path('saved/my/', views.MySavedVideosView.as_view(), name='my-saved'),
]