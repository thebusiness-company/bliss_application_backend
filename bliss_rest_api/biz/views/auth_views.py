from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from rest_framework import status
from ..services.user_service import *
from ..models import *
from rest_framework.decorators import authentication_classes, permission_classes
from django.utils import timezone
  
import datetime

@authentication_classes([])
@permission_classes([])
class CreateToken(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField(write_only=True)
        source = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access, refresh  = create_token(**serializer.validated_data)
        return Response({'access': access, 'refresh': refresh },status=status.HTTP_200_OK)

@authentication_classes([])
@permission_classes([])    
class AddCustomer(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        email = serializers.CharField()
        mobile = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = create_customer(**serializer.validated_data)
        return Response({'data' : customer},status=status.HTTP_200_OK)

class GetUserId(APIView):

    def get(self, request):
        customer = get_user_id(request.user.id)

        return Response({'data' : customer},status=status.HTTP_200_OK)
    
# @authentication_classes([])
# @permission_classes([])       
class GetCustomer(APIView):
    def get(self, request):
        customer = get_customer(request.user.id)
        return Response({'data' : customer},status=status.HTTP_200_OK)    

@authentication_classes([])
@permission_classes([]) 
class ListCustomer(APIView):
    def get(self, request):
        customer = list_customer()
        return Response({'data' : customer},status=status.HTTP_200_OK)     

class UpdateCustomer(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        email = serializers.CharField()
        mobile = serializers.IntegerField()
        address = serializers.CharField()
        city = serializers.CharField()
        state = serializers.CharField()
        country = serializers.CharField()
        pincode = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = update_customer(request.user.id,**serializer.validated_data)
        return Response({'data' : customer},status=status.HTTP_200_OK)
                        
@authentication_classes([])
@permission_classes([])   
class AddCollectionQuery(APIView):
    class InputSerializer(serializers.Serializer):
        key = serializers.CharField()
        query = serializers.CharField()
    
    def post(self,request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        Cq = create_collection_query(**serializer.validated_data)
        return Response({'data': "success"},status=status.HTTP_201_CREATED)
        
@authentication_classes([])
@permission_classes([]) 
class AddRole(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()
        display_value = serializers.CharField()
        code  = serializers.CharField()

    def post(self,request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        add = create_role(**serializer.validated_data)
        return Response({'data': add},status=status.HTTP_201_CREATED)      


@authentication_classes([])
@permission_classes([])    
class AddAdmin(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        email = serializers.CharField()
        mobile = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = create_admin(**serializer.validated_data)
        return Response({'data' : customer},status=status.HTTP_200_OK)          

class Get_User_Role(APIView): 
    def get(self, request):
        customer = get_user_role(request.user.id)
        return Response({'data' : customer},status=status.HTTP_200_OK)     

@authentication_classes([])
@permission_classes([])
class Contact_Submission(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        email = serializers.CharField()
        mobile = serializers.IntegerField()
        message = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        messaging = contact_us(**serializer.validated_data)
        return Response({'data' : messaging},status=status.HTTP_200_OK)   

@authentication_classes([])
@permission_classes([])
class SignInWith_Google(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        email = serializers.CharField()
        sub = serializers.CharField() 
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access, refresh  = signin_via_google(**serializer.validated_data)
        # customer = signin_via_google(**serializer.validated_data)
        return Response({'access': access, 'refresh': refresh },status=status.HTTP_200_OK)   
        
@authentication_classes([])
@permission_classes([])
class Reset_Password(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.CharField()
        path = serializers.CharField()
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_response = reset_user_password(**serializer.validated_data)
        print(reset_response)
        return Response({'data' : reset_response},status=status.HTTP_200_OK) 

@authentication_classes([])
@permission_classes([])
class Change_Password(APIView):
    class InputSerializer(serializers.Serializer):
        userId = serializers.CharField()
        password = serializers.CharField()
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_response = change_user_password(**serializer.validated_data)
        return Response({'data' : reset_response},status=status.HTTP_200_OK)      


