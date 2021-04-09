import jwt
from django.conf import settings
import string
import random
from datetime import datetime, timedelta
from .models import CustomUser
from django.db.models import Q
import re


class JWTToken:
    @staticmethod
    def get_random(length):
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def get_access(payload):
        return jwt.encode({"exp": datetime.now() + timedelta(minutes=5), **payload}, settings.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def get_refresh():
        return jwt.encode({"exp": datetime.now() + timedelta(days=365), "data": JWTToken.get_random(10)}, settings.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
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
        
        return None

        

def get_query(query_string, search_fields):
    query = None  
    terms = normalize_query(query_string)
    
    for term in terms:
        or_query = None 
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]