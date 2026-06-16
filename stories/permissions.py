from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = getattr(obj, 'user', None)
        return user == request.user


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = getattr(obj, 'user', None)
        return user == request.user


class IsAuthenticatedAndOwner(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = getattr(obj, 'user', None)
        return user == request.user