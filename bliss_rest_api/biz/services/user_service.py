import datetime
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
# from rest_framework_simplejwt.authentication import JWTAuthenticationMiddleware
from django.contrib.auth import authenticate
from django.conf import settings
from ..models import *
import uuid
from ..services.collection_query_service import exec_raw_sql
from django.utils import timezone
from bliss_rest_api import settings
from django.core.mail import EmailMessage
# main function 
def create_token(**data):
    user = authenticate(username=data.get('username'), password=data.get('password'))
    if not user:
        raise AuthenticationFailed(detail='Invalid Credentials')

    refresh_tkn = RefreshToken.for_user(user)
    access_tkn = refresh_tkn.access_token
    return str(access_tkn), str(refresh_tkn) 

def create_customer(**data):
    try:
        password = data.get('password')
        user = User.objects.create_user(data.get('email'),data.get('email'),password)
        email = data.get("email")
        user.is_active=True
        # user.validate_token = User.objects.make_random_password(10) + uuid.uuid4().hex[:6].upper()
        user_id = user.id
        role = Role.objects.filter(name = 'customer').first()
        user.roles.add(role.id) #here 1 is role_id of customer refer role table
        user.save()

        # entry in customer_details

        CustomerDetails.objects.create(customer_name = data.get('username'),email = data.get('email'),mobile_number = data.get('mobile'),
                                       user_id = user.id)
        return user.id
    except Exception as e:
        raise APIException(e)

def signin_via_google(**data):
    try:
        # User = get_user_model()
        email = data.get('email')
        name = data.get('name')
        user_exist = User.objects.filter(email = email).first()
        if user_exist is not None:
            # user = User.objects.get(email=email) 
            refresh_tkn = RefreshToken.for_user(user_exist)
            access_tkn = refresh_tkn.access_token

        else :
            user = User.objects.create_user( email,email)
            user.is_active=True
            # user.validate_token = User.objects.make_random_password(10) + uuid.uuid4().hex[:6].upper()
            user_id = user.id
            role = Role.objects.filter(name = 'customer').first()
            user.roles.add(role.id) #here 1 is role_id of customer refer role table
            user.save()
            # auth_login(request, user)
            CustomerDetails.objects.create(customer_name = name,email = email,
                                        user_id = user.id)
            refresh_tkn = RefreshToken.for_user(user)
            access_tkn = refresh_tkn.access_token    
        return str(access_tkn), str(refresh_tkn)    
    except Exception as e:
        raise APIException(e)

def create_admin(**data):
    try:
        password = data.get('password')
        admin = User.objects.create_user(data.get('email'),data.get('email'),password)
        email = data.get("email")
        admin.is_active=True
        # admin.validate_token = User.objects.make_random_password(10) + uuid.uuid4().hex[:6].upper()
        admin_id = admin.id
        role = Role.objects.filter(name = 'admin').first()
        admin.roles.add(role.id) #here 2 is role_id of admin refer role table
        admin.save()
        return admin.id
    except Exception as e:
        raise APIException(e)
       

def get_user_id(user_id):
    try:
        return f'your user id is {user_id}'
    except Exception as e:
        raise APIException(e)
    

# def get_customer(user_id):
#     try:
#         data = exec_raw_sql('I_GET_CUSTOMER_DETAILS', {"id" : user_id}) 
#         print(data)
#         return data
#     except Exception as e:
#         raise APIException(e)        

def get_user_role(user_id):
    try:
        data = exec_raw_sql('GET_USER_ROLE', {"user_id" : user_id}) 
        return data
    except Exception as e:
        raise APIException(e) 

def get_customer(userid): 
    try:
        Customer = CustomerDetails.objects.filter(user_id = userid).values().first()
        return Customer
    except Exception as e:
        raise APIException(e)       

def list_customer(): 
    try:
        Customer = CustomerDetails.objects.all().values()
        return Customer
    except Exception as e:
        raise APIException(e)     

def update_customer(user_id,**data):
    try:
        user= User.objects.filter(id=user_id).first()
        user.username=data.get('email')
        user.email=data.get('email')
        user.save()
        Customer = CustomerDetails.objects.filter(user_id = user_id).first()
        Customer.customer_name = data.get('name')
        Customer.email = data.get('email')
        Customer.address = data.get('address')
        Customer.city = data.get('city')
        Customer.state = data.get('state')
        Customer.country = data.get('country')
        Customer.pincode = data.get('pincode')
        Customer.mobile_number = data.get('mobile')
        Customer.save()
        return "Succesfully updated"
    except Exception as e:
        raise APIException(e)                  
    
def create_collection_query(**data):
    try:
        collection_query = CollectionQuery()
        collection_query.key = data.get('key')
        collection_query.query = data.get('query')
        collection_query.save()
        return collection_query
    except Exception as e:
        raise APIException(e)

def create_role(**data):
    try:
        role = Role.objects.create(name = data.get('name'),description = data.get('description'),display_value = data.get('display_value'),
                            code = data.get('code'), role_cat = data.get('role_cat'))
        return role.id
    except Exception as e:
        raise APIException(e)        

def contact_us(**data):
    try:
        contact = ContactSubmission.objects.create(name = data.get('name'),email = data.get('email'),mobile_number = data.get('mobile'),
                            message = data.get('message'))
        return contact.name
    except Exception as e:
        raise APIException(e)                    
   
def reset_user_password(**data):
    try:
        email = data.get('email')
        path = data.get('path')
        user_exist = User.objects.filter(email = email,is_active = True).first()
        if user_exist is not None:
            mail_subject = "User password reset request"
            to_email = user_exist.email
            from_email = settings.EMAIL_HOST_USER
            link_message = path + '/change-password/' + str(user_exist.id)
            html_message = f'<p>Hello customer,</p> <p>You have requested to reset you password for the bliss application.</p> <p>Please ignore the e-mail, if it is not done by you.</p> <p>Your password reset link is {link_message}</p><p>This is a system genereated e-mail. Do not reply to this e-mail</p>'

            # send_mail(
            #     subject=mail_subject,
            #     message = html_message,
            #     from_email= settings.EMAIL_HOST_USER,
            #     recipient_list=[to_email],
            #     fail_silently = False
            # )
            mail_status = EmailMessage(
                            mail_subject,
                            html_message,
                            from_email,
                            [to_email])
            mail_status.content_subtype = 'html'  # Set the content type as HTML
            mail_status.send()
        return 'Mail sent successfully'    
    except Exception as e:
        raise APIException(e) 
        
def change_user_password(**data):
    try:
        userId = data.get('userId')
        password = data.get('password')
        user_exist = User.objects.filter(id = userId).first()
        if user_exist :
            user_exist.set_password(password)
            user_exist.save()
        return 'Password changed successfully'    
    except Exception as e:
        raise APIException(e)
