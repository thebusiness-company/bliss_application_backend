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
import random


def order_creation(user_id,username,**data):
    try:
        get_customer_id = CustomerDetails.objects.filter(user_id = user_id).first()
        order_creation = Order(product_id = data.get('product_id'),quantity = data.get('quantity'),
                           email = data.get('email'),phone = data.get('phone'),address = data.get('address'),
                           city = data.get('city'),state = data.get('state'),
                           country = data.get('country'),pincode = data.get('pincode'),total_price = data.get('total_price'),
                           tracking_no = 'BLISS' + str(random.randint(1111111,9999999)),payment_mode=data.get('payment_mode'),
                           customer_id = get_customer_id.id,created_by = username )
        order_creation.save()
        return order_creation.id
    except Exception as e:
        raise APIException(e)
    
def order_cancellation(user_id,username,**data):
    try:
        order_data= Order.objects.filter(customer = user_id,id=data.get('order_id')).first()
        order_data.delete()
        return order_data
    except Exception as e:
        raise APIException(e)

def order_updation(user_id,username,**data):
    try:
        order_data= Order.objects.filter(customer = user_id,id=data.get('order_id')).first()
        order_data.email = data.get('email'),
        order_data.phone = data.get('phone'),
        order_data.address = data.get('address'),
        order_data.city = data.get('city'),
        order_data.state = data.get('state'),
        order_data.country = data.get('country'),
        order_data.pincode = data.get('pincode'),
        updated_by = username,
        order_data.save()
        return order_data
    except Exception as e:
        raise APIException(e)

def order_list_byuser(user_id,username,**data):
    try:
        order_data= Order.objects.filter(customer = user_id).values()
        return order_data
    except Exception as e:
        raise APIException(e)

def list_all_orders():
    try:
        order_data= Order.objects.all().values()
        return order_data
    except Exception as e:
        raise APIException(e)        

def get_order_details(user_id):
    try:
        print(user_id)
        data = exec_raw_sql('I_GET_ORDER_DETAILS',{'id' : user_id})
        print(data)
        return data
    except Exception as e:
        raise APIException(e)        