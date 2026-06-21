from rest_framework.permissions import BasePermission

class IsExpert(BasePermission):
    def has_permission(
        self,
        request,
        view,
    ):
        return (
            request.user.is_authenticated
            and request.user.is_expert
        )

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return (
            request.user.is_authenticated
            and request.user.is_expert
        )