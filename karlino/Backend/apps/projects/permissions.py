from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProjectOwnerOrCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if obj.creator_id == request.user.id:
            return True

        if obj.company and obj.company.owner_id == request.user.id:
            return True

        return False