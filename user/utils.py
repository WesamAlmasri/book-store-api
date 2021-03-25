import jwt
from django.conf import settings
import string
import random
from datetime import datetime, timedelta
from .models import CustomUser


def get_random(length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class JWTToken:

    def get_access(payload):
        return jwt.encode({"exp": datetime.now() + timedelta(minutes=5), **payload}, settings.SECRET_KEY, algorithm='HS256')

    def get_refresh():
        return jwt.encode({"exp": datetime.now() + timedelta(days=365), "data": get_random(10)}, settings.SECRET_KEY, algorithm='HS256')
    
    def decode(data):
        if not data:
            return None
        
        token = data[7:]
        decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms='HS256')

        if decoded:
            try:
                return CustomUser.objects.get(id=decoded['user_id'])
            except Exception:
                return None

        