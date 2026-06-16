from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoriesViewSet, ActualnostViewSet, ArchiveViewSet

router = DefaultRouter()
router.register(r'stories', StoriesViewSet, basename='stories')
router.register(r'actualnost', ActualnostViewSet, basename='actualnost')
router.register(r'archive', ArchiveViewSet, basename='archive')

urlpatterns = [
    path('', include(router.urls)),
]