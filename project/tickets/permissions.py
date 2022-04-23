from rest_framework import permissions

class IsAutherOrReedOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return obj.auther== request.user
