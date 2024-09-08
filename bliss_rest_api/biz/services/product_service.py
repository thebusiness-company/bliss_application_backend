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
from django.db import transaction

@transaction.atomic()
def create_product(username,**data):
    try:
        add_product = Product(product_name = data.get('product_name'),
                              selling_price = data.get('selling_price'),
                              original_price = data.get('original_price'),
                              description = data.get('description'),
                              quantity = data.get('quantity'),
                              created_by = username,
                              )
        
        # fl_upd = FileUpload.objects.filter(tmp_file_name=data.get('product_image')).first()
        # if fl_upd is not None:
        #     disp_name = get_random_string(length=12) + "_" + fl_upd.orig_file_name
        #     dest_file_name = 'storage/products/snaps' 
        #     fl_upd.storage_file_name = dest_file_name + disp_name
        #     fl_upd.save()
        #     add_product.product_image = fl_upd.storage_file_name
        #     # insurance_provider.save()
        #     move_tmp_file(fl_upd.id)   
        # add_product.save()
        # return add_product.product_name
        temp_images_container = data.get('product_image')
        original_images_container = []
        for i in range(len(temp_images_container)):
            fl_upd = FileUpload.objects.filter(tmp_file_name=temp_images_container[i]).first()
            if fl_upd is not None:
                disp_name = get_random_string(length=12) + "_" + fl_upd.orig_file_name
                dest_file_name = 'storage/bliss/products/'
                fl_upd.storage_file_name = dest_file_name + disp_name
                fl_upd.save()
                original_images_container.append(fl_upd.storage_file_name)
                move_tmp_file(fl_upd.id)
        
        add_product.product_image = original_images_container
        add_product.save()
        return add_product.product_name
    except Exception as e:
        raise APIException(e)        
    
def get_product(**data):
    try:
        product = Product.objects.filter(id = data.get('product_id')).values().first()
        return product
    except Exception as e:
        raise APIException(e)

def list_products(**data):
    try:
        product = Product.objects.all().values()
        return product
    except Exception as e:
        raise APIException(e)   

def update_product(username,**data):
    try:
        product = Product.objects.filter(id=data.get('product_id')).first()
        product.product_name =  data.get('product_name')
        product.quantity= data.get('quantity')
        product.original_price= data.get('original_price')
        product.selling_price= data.get('selling_price')
        product.description= data.get('description')
        # product.status = data.get('status')
        product.trending= data.get('trending')
        # product_image= data.get('product_image')
        product.availability= data.get('availability')
        product.updated_by = username
        temp_images_container = data.get('product_image')
        original_images_container = []
        for i in range(len(temp_images_container)):
            fl_upd = FileUpload.objects.filter(tmp_file_name=temp_images_container[i]).first()
            if fl_upd is not None:
                disp_name = get_random_string(length=12) + "_" + fl_upd.orig_file_name
                dest_file_name = 'storage/bliss/products/'
                fl_upd.storage_file_name = dest_file_name + disp_name
                fl_upd.save()
                original_images_container.append(fl_upd.storage_file_name)
                move_tmp_file(fl_upd.id)
        
        product.product_image = original_images_container
        product.save()
        return product.id
    except Exception as e:
        raise APIException(e)  

def delete_product(**data):
    try:
        product = Product.objects.filter(id=data.get('product_id'))
        product.delete()

        return "Success"
    except Exception as e:
        raise APIException(e) 





            


        