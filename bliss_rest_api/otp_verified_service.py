import json
from ..models import *
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import APIException
from datetime import date,datetime, timedelta
from django.contrib.auth.hashers import check_password
import logging
from adm.services.collection_query_service import exec_raw_sql
from adm.services.metals_service import *
#from ..services.celery_task import send_mail_func
from django.utils import timezone
from adm.models import *
from inv.models import * 
from inv.models.student import Student
from django.db import transaction,IntegrityError
import random
from ..tasks.task import *
from inv.services.wallet_transactions_service import *
import re

logger = logging.getLogger('django')


# @transaction.atomic()
def validate_email(username,**data):
    try:
        validate_email = User.objects.filter(email = data.get('email_id'),is_active = True).first()
        if validate_email is not None:
            new_otp = random.randint(100000, 999999)
            # new entry in otp_verified
            current_time = datetime.now()
            new_entry = OTPVerified.objects.create(user_id = data.get('user_id'),email_id = data.get('email_id'),otp = int(new_otp),
                                                   otp_sent_time = current_time,expired_in_min = 5,created_by = username)
            # mail has to be sent
            #mailer_queue.enqueue(otp_sent_for_forget_password,args=(new_otp,data.get('email_id'),data.get('user_id')))
            otp_sent_for_forget_password(new_otp,data.get('email_id'),data.get('user_id'))
            data = {}
            data.update({"message" : "Email verified Successfully & OTP was sent please check your mail",
                         "otp_id" : new_entry.id ,"otp" : new_otp,
                         "user_id" : validate_email.id})
            # message = ("Email verified Successfully & OTP was sent please check your mail")
            return data
        else:
            raise APIException('Please enter your email ID on which the registration link was sent from FinSmiles')


    except Exception as e:
        raise APIException (str(e))
    
def otp_verify(username,**data):
    try:
        user = User.objects.filter(email = data.get('email_id')).first()
        current_time = timezone.now()
        otp,otp_id = data.get("otp"),data.get("otp_id")
        c_year,c_month,c_day,c_hour,c_minute,c_second = current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second
        latest = OTPVerified.objects.filter(email_id = data.get("email_id"),id = data.get("otp_id")).first()
        otp_sent_time = latest.otp_sent_time
        otp_year,otp_month,otp_day,otp_hour,otp_minute,otp_second = otp_sent_time.year,otp_sent_time.month,otp_sent_time.day,otp_sent_time.hour,otp_sent_time.minute,otp_sent_time.second
        first_datetime = timezone.datetime(otp_year,otp_month,otp_day,otp_hour,otp_minute,otp_second, tzinfo=timezone.utc)
        second_datetime = timezone.datetime(c_year,c_month,c_day,c_hour,c_minute,c_second, tzinfo=timezone.utc)
        # new_entry for verify
        new_entry = OTPVerified.objects.filter(id = otp_id).first()
        new_entry.verified_otp_time = current_time
        
        # Calculate the difference in minutes
        minutes_difference = (second_datetime - first_datetime).total_seconds() / 60
        data={}
        # Check if the difference is 5 minutes or greater
        if otp != new_entry.otp:
            data.update({"message" : "You have entered the wrong OTP","verify" : False,"user_id" : user.id})

        elif minutes_difference >= 5:
            # raise APIException("Your OTP was expired")
            data.update({"message" : "Your OTP was expired","verify" : False,"user_id" : user.id})
        else:
            new_entry.save()
          
            data.update({"message" : "OTP Verified successfully",
                         "otp_id" : otp_id,
                         "user_id" : user.id,
                         "verify" : True})
            
        return data
    except Exception as e:
        raise APIException (str(e))
    

def set_forget_password(**data):
    try:
        current_time = timezone.now()
        c_year,c_month,c_day,c_hour,c_minute,c_second = current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second
        latest = OTPVerified.objects.filter(id = data.get("otp_id")).first()
        verified_otp_time = latest.verified_otp_time
        otp_year,otp_month,otp_day,otp_hour,otp_minute,otp_second = verified_otp_time.year,verified_otp_time.month,verified_otp_time.day,verified_otp_time.hour,verified_otp_time.minute,verified_otp_time.second
        first_datetime = timezone.datetime(otp_year,otp_month,otp_day,otp_hour,otp_minute,otp_second, tzinfo=timezone.utc)
        second_datetime = timezone.datetime(c_year,c_month,c_day,c_hour,c_minute,c_second, tzinfo=timezone.utc)
        
        # Calculate the difference in minutes
        minutes_difference = (second_datetime - first_datetime).total_seconds() / 60
        if minutes_difference >= 5:
            raise APIException("You are taking too much time,Try again")
        
        user = User.objects.filter(id=data.get('user_id')).first()
        if user is None:
            raise APIException('User not available')
        if data.get('new_password') != data.get('confirm_password'):
            raise APIException("New password doesnt match with confirm password")
        #c = data.get('new_password')
        password_pattern_validation(data.get("confirm_password"))
        user.set_password(data.get('new_password'))
        user.save()
        return ({"message" : "Password set successfully","user_id" : user.id})
    except Exception as e:
        raise APIException (str(e))


def change_password(**data):
    try:
        user = User.objects.filter(id= data.get("user_id")).first()
        # Check if the provided password matches the hashed password in the database
        
        if (data.get("new_password")) != (data.get("confirm_password")):
            raise APIException("New password dont match with confirm password")
        
        else:
        
            password_matched = user.check_password(data.get("old_password"))
            
            # password validation  check
            
            if password_matched:
                password_pattern_validation(data.get("confirm_password"))
                if data.get('new_password')==data.get('old_password'):
                    raise APIException ("This password is already exists")
                else:
                    user.set_password(data.get('new_password'))
                    user.save()
            else:
                raise APIException ("Current password does not match with your actual password")
        return ({"message" : "Password changed Successfully","user_id" : user.id})

    except Exception as e:
        raise APIException(str(e))

def password_pattern_validation(password):
    try:
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.Please follow the password policy and create a strong password')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.Please follow the password policy and create a strong password')
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one digit.Please follow the password policy and create a strong password')
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError('Password must contain at least one special character.Please follow the password policy and create a strong password')
        else:
            return "done"
    
    except Exception as e:
        raise APIException(str(e))
    

def validate_email_for_firstlogin(username,**data):
    try:
        validate_email = User.objects.filter(email = data.get('email_id'),is_active = True).first()
        if validate_email is not None:
            new_otp = random.randint(100000, 999999)
            # new entry in otp_verified
            current_time = datetime.now()
            new_entry = OTPVerified.objects.create(user_id = data.get('user_id'),email_id = data.get('email_id'),otp = int(new_otp),
                                                   otp_sent_time = current_time,expired_in_min = 5,created_by = username)
            # mail has to be sent
            #mailer_queue.enqueue(otp_sent_for_forget_password,args=(new_otp,data.get('email_id'),data.get('user_id')))
            otp_sent_for_forget_password(new_otp,data.get('email_id'),data.get('user_id'))
            data = {}
            data.update({"message" : "Email verified Successfully & OTP was sent please check your mail",
                         "otp_id" : new_entry.id ,"otp" : new_otp,
                         "user_id" : validate_email.id})
            # message = ("Email verified Successfully & OTP was sent please check your mail")
            return data
        else:
            raise APIException('Please enter your email ID on which the registration link was sent from FinSmiles')


    except Exception as e:
        raise APIException (str(e))
    
def otp_verify_for_firstlogin(username,**data):
    try:
        user = User.objects.filter(email = data.get('email_id')).first()
        current_time = timezone.now()
        otp,otp_id = data.get("otp"),data.get("otp_id")
        c_year,c_month,c_day,c_hour,c_minute,c_second = current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second
        latest = OTPVerified.objects.filter(email_id = data.get("email_id"),id = data.get("otp_id")).first()
        otp_sent_time = latest.otp_sent_time
        otp_year,otp_month,otp_day,otp_hour,otp_minute,otp_second = otp_sent_time.year,otp_sent_time.month,otp_sent_time.day,otp_sent_time.hour,otp_sent_time.minute,otp_sent_time.second
        first_datetime = timezone.datetime(otp_year,otp_month,otp_day,otp_hour,otp_minute,otp_second, tzinfo=timezone.utc)
        second_datetime = timezone.datetime(c_year,c_month,c_day,c_hour,c_minute,c_second, tzinfo=timezone.utc)
        # new_entry for verify
        new_entry = OTPVerified.objects.filter(id = otp_id).first()
        new_entry.verified_otp_time = current_time
        
        # Calculate the difference in minutes
        minutes_difference = (second_datetime - first_datetime).total_seconds() / 60
        data={}
        # Check if the difference is 5 minutes or greater
        if otp != new_entry.otp:
            data.update({"message" : "You have entered the wrong OTP","verify" : False,"user_id" : user.id})

        elif minutes_difference >= 5:
            # raise APIException("Your OTP was expired")
            data.update({"message" : "Your OTP was expired","verify" : False,"user_id" : user.id})
        else:
            new_entry.save()
          
            data.update({"message" : "OTP Verified successfully",
                         "otp_id" : otp_id,
                         "user_id" : user.id,
                         "verify" : True})
            
        return data
    except Exception as e:
        raise APIException (str(e))
    

def set_forget_password_for_firstlogin(**data):
    try:
        current_time = timezone.now()
        c_year,c_month,c_day,c_hour,c_minute,c_second = current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second
        latest = OTPVerified.objects.filter(id = data.get("otp_id")).first()
        verified_otp_time = latest.verified_otp_time
        otp_year,otp_month,otp_day,otp_hour,otp_minute,otp_second = verified_otp_time.year,verified_otp_time.month,verified_otp_time.day,verified_otp_time.hour,verified_otp_time.minute,verified_otp_time.second
        first_datetime = timezone.datetime(otp_year,otp_month,otp_day,otp_hour,otp_minute,otp_second, tzinfo=timezone.utc)
        second_datetime = timezone.datetime(c_year,c_month,c_day,c_hour,c_minute,c_second, tzinfo=timezone.utc)
        
        # Calculate the difference in minutes
        minutes_difference = (second_datetime - first_datetime).total_seconds() / 60
        if minutes_difference >= 5:
            raise APIException("You are taking too much time,Try again")
        
        user = User.objects.filter(id=data.get('user_id')).first()
        if user is None:
            raise APIException('User not available')
        if data.get('new_password') != data.get('confirm_password'):
            raise APIException("password do not match")
        
        password_pattern_validation(data.get("confirm_password"))
        #c = data.get('new_password')
        user.set_password(data.get('new_password'))
        user.save()
        return ({"message" : "Password set successfully","user_id" : user.id})
    except Exception as e:
        raise APIException (str(e))


def change_password_for_firstlogin(**data):
    try:
        user = User.objects.filter(id= data.get("user_id")).first()
        # Check if the provided password matches the hashed password in the database
        
        if (data.get("new_password")) != (data.get("confirm_password")):
            raise APIException("New password dont match with confirm password")
        
        else:
        
            password_matched = user.check_password(data.get("old_password"))
            
            # password validation  check
            
            if password_matched:
                password_pattern_validation(data.get("confirm_password"))
                if data.get('new_password')==data.get('old_password'):
                    raise APIException ("This password is already exists")
                else:
                    user.set_password(data.get('new_password'))
                    user.save()
            else:
                raise APIException ("The old password donot match the user's password.")
        return ({"message" : "Password changed Successfully","user_id" : user.id})

    except Exception as e:
        raise APIException(str(e))
    
def set_password_for_firstlogin(**data):
    try:
        user = User.objects.filter(id= data.get("user_id")).first()
        # Check if the provided password matches the hashed password in the database
        
        if (data.get("new_password")) != (data.get("confirm_password")):
            raise APIException("New password dont match with confirm password")
            
            # password validation  check
        else:
            password_pattern_validation(data.get("confirm_password"))
            user.set_password(data.get('new_password'))
            # status changing
            user.save()
            # exec_raw_sql('STUDENT_FIRST_LOGIN_STATUS_CHANGED',{'id' : get_student_id(data.get("user_id"))})
            student_status = Student.objects.filter(user_id = data.get('user_id')).first()
            student_status.first_login_status = 'Completed'
            student_status.save()
            
            
          
        return ({"message" : "Password set Successfully","user_id" : user.id})

    except Exception as e:
        raise APIException(str(e))