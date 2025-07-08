from rest_framework import permissions
from .models import User, Order

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.ADMIN

class IsDeliveryMan(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.DELIVERY_MAN

class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # User can access only their own orders
        return obj.user == request.user
