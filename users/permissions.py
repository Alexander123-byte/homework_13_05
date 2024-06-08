from rest_framework import permissions


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsNotModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moders").exists()


class IsOwnerOrModer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.owner
            or request.user.groups.filter(name="moders").exists()
        )
