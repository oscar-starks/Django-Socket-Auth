from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from accounts.custom_functions import decodeJWT

class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        http_auth = request.META.get("HTTP_AUTHORIZATION")
        if not http_auth:
            raise AuthenticationFailed("Auth token not provided!")
        try:
            user = decodeJWT(http_auth)
        except:
            raise AuthenticationFailed("Auth token invalid or expired!")
        
        if not user:
            raise AuthenticationFailed("Auth token invalid or expired!")
        request.user = user
        if request.user and request.user.is_authenticated:
            return True
        return False
    

