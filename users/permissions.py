from rest_framework import permissions


class IsModer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
