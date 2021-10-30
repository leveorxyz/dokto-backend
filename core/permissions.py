from rest_framework.permissions import BasePermission
from user.models import User


class PatientPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == User.UserType.PATIENT)


class DoctorPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == User.UserType.DOCTOR)


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == User.UserType.ADMIN)


class CollectivePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == User.UserType.COLLECTIVE)


class PharmacyPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == User.UserType.PHARMACY)


class OwnProfilePermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
