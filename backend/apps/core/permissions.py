from rest_framework.permissions import BasePermission
from .constants import MANAGER_GROUP, DELIVERY_CREW_GROUP, KITCHEN_STAFF_GROUP, SAFE_METHODS

class BaseGroupPermission(BasePermission):
    group_name = None
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name=self.group_name).exists()

class RoleOrReadOnlyPermission(BaseGroupPermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)

class IsManager(BaseGroupPermission):
    group_name = MANAGER_GROUP

class IsDeliveryCrew(BaseGroupPermission):
    group_name = DELIVERY_CREW_GROUP

class IsKitchenStaff(BaseGroupPermission):
    group_name = KITCHEN_STAFF_GROUP

class IsManagerOrReadOnly(RoleOrReadOnlyPermission):
    group_name = MANAGER_GROUP