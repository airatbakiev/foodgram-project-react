from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_staff
            or view.action == 'retrieve'
        )


class RecipeAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_staff
        )


class SubscribeOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user
            or request.user.is_staff
        )


class UserMeOrUserProfile(permissions.BasePermission):

    def has_permission(self, request, view):
        user_me = bool(
            request.user
            and request.user.is_authenticated
            and request.path_info == '/api/users/me/'
        )
        user_profile = bool(
            request.path_info != '/api/users/me/'
        )
        return bool(user_me or user_profile)
