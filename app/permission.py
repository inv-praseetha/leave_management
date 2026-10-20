from django.core.mail import message
from rest_framework.permissions import BasePermission
from .models import User
class IsAdmin(BasePermission):
    message = "Only admin can access this API."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = "Please login first."
            return False

        if request.user.role != User.Role.ADMIN:
            self.message = "You are not authorized to access this API."
            return False

        return True
class IsEmployee(BasePermission):
    message = "Only admin can access this API."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = "Please login first."
            return False

        if request.user.role != User.Role.EMPLOYEE:
            self.message = "You are not authorized to access this API."
            return False

        return True
class IsManager(BasePermission):
    def has_permission(self,request,view):
        if not request.user.is_authenticated:
            self.message = "Please login first."
            return False

        if request.user.role != User.Role.MANAGER:
            self.message = "You are not authorized to access this API."
            return False

        return True
        
