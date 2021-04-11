from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.utils import timezone



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

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
    
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user

class IsAutherBookOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
    
        if request.method in SAFE_METHODS:
            return True

        return obj.auther.user == request.user

class IsImageOwnerOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
    
        if request.method in SAFE_METHODS:
            return True

        return obj.book.auther.user == request.user
        
def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        return response
    
    exc_list = str(exc).split('DETAIL: ')

    return Response({'error': exc_list}, status=403)