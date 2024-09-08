from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from rest_framework import status
from ..services.cart_service import *
from ..models import *
from rest_framework.decorators import authentication_classes, permission_classes
from django.utils import timezone 
import datetime

# @authentication_classes([])
# @permission_classes([]) 
class AddCart(APIView):
    class InputSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        product_qty = serializers.IntegerField()
        # customer_id = serializers.IntegerField()
        # created_by = serializers.CharField()
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = add_to_cart(request.user.id,request.user.username,**serializer.validated_data)
        return Response({'data' : product },status=status.HTTP_200_OK)

# @authentication_classes([])
# @permission_classes([]) 
class GetCart(APIView):
    class InputSerializer(serializers.Serializer):
        cart_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_cart_items(request.user.id,**serializer.validated_data)
        return Response({'data' : product },status=status.HTTP_200_OK)    

# @authentication_classes([])
# @permission_classes([]) 
class ListCartItems(APIView):
    # class InputSerializer(serializers.Serializer):
    #     user_id = serializers.IntegerField()
        
    def get(self, request):
        # serializer = self.InputSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        product = list_cart_items(request.user.id)
        return Response({'data' : product },status=status.HTTP_200_OK)

# @authentication_classes([])
# @permission_classes([]) 
class UpdateCartItems(APIView): 
    class InputSerializer(serializers.Serializer):
        cart_id = serializers.IntegerField()
        product_qty = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = update_cart_items(request.user.id,**serializer.validated_data)
        return Response({'data' : product },status=status.HTTP_200_OK)      

# @authentication_classes([])
# @permission_classes([])         
class DeleteCartItems(APIView): 
    class InputSerializer(serializers.Serializer):
        # user_id = serializers.IntegerField()
        cart_id = serializers.IntegerField()
        # product_qty = serializers.IntegerField()
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = delete_cart_items(request.user.id,**serializer.validated_data)
        return Response({'data' : product },status=status.HTTP_200_OK)    

# @authentication_classes([])
# @permission_classes([]) 
class DeleteAllItems(APIView): 
    def delete(self, request):
        product = remove_all_cart_items_for_customer(request.user.id)
        return Response({'data' : product },status=status.HTTP_200_OK)         