import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from datetime import datetime

class Authentication(BaseAuthentication):

    def authenticate(self, request):
        data = self.validate_request(request.headers)
        
        if not data:
            return None, None
        
        user = self.get_user(data['user_id'])

        return user, None
    

    def validate_request(self, headers):
        authorization = headers.get('Authorization', None)

        if not authorization:
            return None
        
        decoded_data = self.verify_token(authorization[7:])

        if not decoded_data:
            return None
        
        return decoded_data
    
    @staticmethod
    def verify_token(token):
        decoded_data = jwt.decode(token, key=settings.SECRET_KEY, algorithms='HS256')

        if not decoded_data:
            return None

        exp = decoded_data['exp']

        if datetime.now().timestamp() > exp:
            return None
        
        return decoded_data


    def get_user(user_id):
        try:
            from .models import CustomUser
            user = CustomUser.objects.get(id=user_id)
            return user
        except Exception:
            return None