from rest_framework import permissions


class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверка, что пользователь принадлежит к группе "Модераторы".
        return request.user.groups.filter(name='Модераторы').exists() and request.method == 'PATCH'
