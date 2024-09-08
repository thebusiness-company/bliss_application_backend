import datetime
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
# from rest_framework_simplejwt.authentication import JWTAuthenticationMiddleware
from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.crypto import get_random_string
from .file_service import *
from .customer_service import *
from ..models import *
import uuid
from ..services.collection_query_service import exec_raw_sql


def add_to_cart(user_id,username,**data):
    try:
            customer_id = get_customer_id(user_id)
            add_to_cart = Cart.objects.create(product_id = data.get('product_id'),product_qty = data.get('product_qty'),
                         customer_id = customer_id,created_by = username)
            add_to_cart.save()
            return "Success"
    except Exception as e:
        raise APIException(e)
    
# def list_cart_items(user_id):
#     try:
#         Cart_items = Cart.objects.filter(customer_id = user_id).values()
#         return Cart_items
#     except Exception as e:
        raise APIException(e)

def list_cart_items(user_id):
    try:
        customer_id = get_customer_id(user_id)
        data = exec_raw_sql('GET_CART_DETAILS', {"id" : customer_id}) 
        return data
    except Exception as e:
        raise APIException(e)    

def get_cart_items(user_id,**data):
    try:
        customer_id = get_customer_id(user_id)
        data = exec_raw_sql('GET_CART_ITEM', {"cart_id" : data.get("cart_id") , "user_id" : customer_id}) 
        return data
    except Exception as e:
        raise APIException(e)         


def update_cart_items(user_id,**data):
    try:
        customer_id = get_customer_id(user_id)
        update_cart = Cart.objects.filter(customer_id = customer_id, id= data.get("cart_id")).first()
        update_cart.product_qty = data.get('product_qty')
        update_cart.save()
        return update_cart.customer_id
    except Exception as e:
        raise APIException(e) 

def delete_cart_items(user_id,cart_id):
    try:
        customer_id = get_customer_id(user_id)
        cart_item = Cart.objects.filter(customer_id = customer_id, id=cart_id)
        cart_item.delete()
        return "Success"
    except Exception as e:
        raise APIException(e)
#
# def delete_all_cart_items(user_id):
#     # try:
#         customer_id = get_customer_id(user_id)
#         print(customer_id)
#         a =  exec_raw_sql('DELETE_ALL_CART_ITEM', {"customer_id" : customer_id})  
#         print(a)
#         print(2)
#         # print(data)
#         return "Success"
#     # except Exception as e:
#     #     raise APIException(e)      

def remove_all_cart_items_for_customer(user_id):
    try:
        customer_id = get_customer_id(user_id)
        Cart.objects.filter(customer_id = customer_id).delete()
        return "Done"
    except Exception as e:
        raise APIException(e)  
    




