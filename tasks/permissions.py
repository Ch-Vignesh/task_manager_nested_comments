# tasks/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnlyTask(permissions.BasePermission):
    """
    Only the owner of the task can edit it.
    """
    """
    Check if the user has permission to perform an action on a specific object.

    This function is used in Django REST framework's permission classes to determine
    whether a user has permission to perform a specific action on a given object.

    Parameters:
    - request (Request): The incoming request object containing information about the user and the requested action.
    - view (View): The view object that is handling the request.
    - obj (Model): The specific object on which the user is trying to perform the action.

    Returns:
    - bool: True if the user has permission to perform the action on the object, False otherwise.
        - For safe HTTP methods (GET, HEAD, OPTIONS), permission is always granted.
        - For other HTTP methods, permission is granted only if the user is the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsAuthorOrReadOnlyComment(permissions.BasePermission):
    """
    Only the author of the comment can edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
