from rest_framework import permissions


class IsOrganiserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer.is_organizer == True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT", "DELETE"]:
            return obj.organizer == request.user
        return True


class IsParticipantInPrivateEvent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_private:
            return request.user in obj.participants_event.all() or request.user == obj.organizer
        return True


class IsOwnerOfferEvent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.desired_event.organizer == request.user


class IsOwnerOfferUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.visitor == request.user
