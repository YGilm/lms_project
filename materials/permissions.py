from rest_framework import permissions


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет модераторам редактировать объекты,
    но ограничивает остальных пользователей только чтением.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Модераторы').exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет только владельцам редактировать свои объекты.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Разрешение, которое позволяет владельцам и модераторам редактировать объекты.
    Пользователи, не входящие в группу модераторов, могут видеть, редактировать и удалять только свои объекты.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_moderator = request.user.groups.filter(name='Модераторы').exists()
        is_owner = obj.owner == request.user
        return is_moderator or is_owner
