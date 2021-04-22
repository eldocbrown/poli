from rest_framework.permissions import BasePermission

import sys

class IsLocationSupervisorOrReadOnly(BasePermission):
    """
    Custom permission to only allow supervisors of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #if request.method in permissions.SAFE_METHODS:
        #    return True

        # Write permissions are only allowed to a supervisor of the object.
        return request.user in obj.where.supervisors.all()

class IsSameUser(BasePermission):

    """
    Custom permission to only same user as requested
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj

class IsSupervisorUser(BasePermission):

    """
    Custom permission to supervisor user in request
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_supervisor
