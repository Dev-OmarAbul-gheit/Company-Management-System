from rest_framework.permissions import BasePermission 

class IsAdmin(BasePermission):
    def has_permission(self, request, view):    
        return request.user.is_authenticated and request.user.role == 'Admin'


class IsManager(BasePermission):
    def __init__(self, allowed_permissions=[]):
        self.allowed_permissions = allowed_permissions

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in self.allowed_permissions:
                return True
        return view.permission_denied(request, message="A manager does not have permission to perform this action.")
        

class IsEmployee(BasePermission):
    def __init__(self, allowed_permissions=[]):
        self.allowed_permissions = allowed_permissions

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in self.allowed_permissions:
                return True
            
        return view.permission_denied(request, message="An employee does not have permission to perform this action.")