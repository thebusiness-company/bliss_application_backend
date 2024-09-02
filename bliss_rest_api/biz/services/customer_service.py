import datetime
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
# from rest_framework_simplejwt.authentication import JWTAuthenticationMiddleware
from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.crypto import get_random_string
from .file_service import *
from ..models import *
import uuid
from ..services.collection_query_service import exec_raw_sql


def get_customer_id(userid) :
    try:
        customer_id = CustomerDetails.objects.filter(user_id = userid).first()
        return customer_id.id    
    except Exception as e:
        raise APIException(e)        
                        

