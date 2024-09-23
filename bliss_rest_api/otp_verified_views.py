from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from rest_framework import status
from adm.services.user_service import *
from adm.services.otp_verified_service import *
#from ..services.token_pair_service import create_token
from ..models import *
from rest_framework.decorators import authentication_classes, permission_classes
from adm.tasks.api_logger_task import log_api_history
# logger = logging.getLogger('django')


@authentication_classes([])
@permission_classes([])
class ValidateEmail(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField(required = True)
        email_id = serializers.EmailField(required = True)      
    def post(self, request):
        #authorize_request('api_buy_mfund',request.user)
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        validate =  validate_email(request.user.username,**serializer.validated_data)
        log_api_history(request.data,{"validate" : "done"},'ValidateEmail', validate['user_id'])
        return Response({"data" : validate},status = status.HTTP_201_CREATED)

@authentication_classes([])
@permission_classes([])
class OTPVerify(APIView):
    class InputSerializer(serializers.Serializer):
        email_id = serializers.EmailField(required = True)   
        otp = serializers.IntegerField(required=True)   
        otp_id = serializers.IntegerField(required=True)  

    def post(self, request):
        #authorize_request('api_buy_mfund',request.user)
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        verify = otp_verify(request.user.username,**serializer.validated_data)
        log_api_history(request.data, {}, 'OTPVerify', verify['user_id'])
        return Response({"data" : verify},status = status.HTTP_201_CREATED)

@authentication_classes([])
@permission_classes([])
class SetForgetPassword(APIView):
    class InputSerializer(serializers.Serializer): 
        otp_id = serializers.IntegerField(required=True)  
        user_id = serializers.IntegerField(required=True)
        new_password = serializers.CharField(required=True)
        confirm_password = serializers.CharField(required=True)

    def post(self, request):
        #authorize_request('api_buy_mfund',request.user)
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        set_password = set_forget_password(**serializer.validated_data)
        log_api_history(request.data, {}, 'SetForgetPassword',set_password['user_id'])
        return Response({"data" : set_password},status = status.HTTP_201_CREATED)
    
class ChangePassword(APIView):
    class InputSerializer(serializers.Serializer): 
        user_id = serializers.IntegerField(required=True)
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)
        confirm_password = serializers.CharField(required=True)

    def post(self, request):
        #authorize_request('api_buy_mfund',request.user)
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        change_pwd = change_password(**serializer.validated_data)
        log_api_history(request.data, {}, 'SetForgetPassword', change_pwd['user_id'])
        return Response({"data" : change_pwd},status = status.HTTP_201_CREATED)
    
#for first login
@authentication_classes([])
@permission_classes([])
class ValidateEmailForFirstLogin(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField(required = True)
        email_id = serializers.EmailField(required = True)      
    def post(self, request):
        #authorize_request('api_buy_mfund',request.user)
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        validate =  validate_email_for_firstlogin(request.user.username,**serializer.validated_data)
        log_api_history(request.data,{"validate" : "done"},'ValidateEmail', validate['user_id'])
        return Response({"data" : validate},status = status.HTTP_201_CREATED)

@authentication_classes([])
@permission_classes([])
class OTPVerifyForFirstLogin(APIView):
    class InputSerializer(serializers.Serializer):
        email_id = serializers.EmailField(required = True)   
        otp = serializers.IntegerField(required=True)   
        otp_id = serializers.IntegerField(required=True)  

    def post(self, request):
        #authorize_request('api_buy_mfund',request.user)
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        verify = otp_verify_for_firstlogin(request.user.username,**serializer.validated_data)
        log_api_history(request.data, {}, 'OTPVerify', verify['user_id'])
        return Response({"data" : verify},status = status.HTTP_201_CREATED)

@authentication_classes([])
@permission_classes([])
class SetForgetPasswordForFirstLogin(APIView):
    class InputSerializer(serializers.Serializer): 
        otp_id = serializers.IntegerField(required=True)  
        user_id = serializers.IntegerField(required=True)
        new_password = serializers.CharField(required=True)
        confirm_password = serializers.CharField(required=True)

    def post(self, request):
        #authorize_request('api_buy_mfund',request.user)
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        set_password = set_forget_password_for_firstlogin(**serializer.validated_data)
        log_api_history(request.data, {}, 'SetForgetPassword',set_password['user_id'])
        return Response({"data" : set_password},status = status.HTTP_201_CREATED)
    
class ChangePasswordForFirstLogin(APIView):
    class InputSerializer(serializers.Serializer): 
        user_id = serializers.IntegerField(required=True)
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)
        confirm_password = serializers.CharField(required=True)

    def post(self, request):
        #authorize_request('api_buy_mfund',request.user)
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        change_pwd = change_password_for_firstlogin(**serializer.validated_data)
        log_api_history(request.data, {}, 'SetForgetPassword', change_pwd['user_id'])
        return Response({"data" : change_pwd},status = status.HTTP_201_CREATED)
    
class SetPasswordForFirstLogin(APIView):
    class InputSerializer(serializers.Serializer): 
        user_id = serializers.IntegerField(required=True)
        new_password = serializers.CharField(required=True)
        confirm_password = serializers.CharField(required=True)

    def post(self, request):
        #authorize_request('api_buy_mfund',request.user)
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        change_pwd = set_password_for_firstlogin(**serializer.validated_data)
        log_api_history(request.data, {}, 'SetForgetPassword', change_pwd['user_id'])
        return Response({"data" : change_pwd},status = status.HTTP_201_CREATED)