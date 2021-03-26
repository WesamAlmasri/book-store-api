from rest_framework.permissions import BasePermission
from rest_framework.response import Response


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        from user.utils import JWTToken
        # user = JWTToken.decode(request.META['HTTP_AUTHORIZATION'])
        from user.models import CustomUser
        user = CustomUser.objects.get(id=1) # just in dev
 
        if not user:
            return False
        
        request.user = user
        
        if request.user and request.user.is_authenticated:
            return True
        
        return False
        