from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from rest_framework import status
from ..services.order_service import *
from ..models import *
from rest_framework.decorators import authentication_classes, permission_classes
from django.utils import timezone 
import datetime


class AddOrder(APIView):
    class InputSerializer(serializers.Serializer):
        customer_name= serializers.CharField()
        product_id = serializers.IntegerField()
        quantity = serializers.IntegerField()
        email = serializers.CharField()
        phone = serializers.IntegerField()
        address = serializers.CharField()
        city = serializers.CharField()
        state=serializers.CharField()
        country= serializers.CharField()
        pincode= serializers.IntegerField()
        total_price = serializers.FloatField()
        payment_mode = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = order_creation(request.user.id,request.user.username,**serializer.validated_data)

        return Response({'data' : product },status=status.HTTP_200_OK)

class CancelOrder(APIView):
    class InputSerializer(serializers.Serializer):
        order_id = serializers.IntegerField()

    def delete(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = order_creation(request.user.id,request.user.username,**serializer.validated_data)

        return Response({'data' : product },status=status.HTTP_200_OK)     

class UpdateOrder(APIView):
    class InputSerializer(serializers.Serializer):
        order_id = serializers.IntegerField()
        product_quantity = serializers.IntegerField()
        email = serializers.CharField()
        phone = serializers.IntegerField()
        address = serializers.CharField()
        city = serializers.CharField()
        state=serializers.CharField()
        country= serializers.CharField()
        pincode= serializers.IntegerField()
        
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = order_updation(request.user.id,request.user.username,**serializer.validated_data)
        return Response({'data' : product },status=status.HTTP_200_OK)   

class GetOrderData(APIView):
    class InputSerializer(serializers.Serializer):
        order_id = serializers.IntegerField()
    def post(self,request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = get_order_details(request.user.id,**serializer.validated_data)
        return Response({'data' : data },status=status.HTTP_200_OK)                

class ListOrdersByUser(APIView):    
    def get(self, request):
        product = order_list_byuser(request.user.id,request.user.username)
        return Response({'data' : product },status=status.HTTP_200_OK) 

class ListAllOrders(APIView):
    def get(self, request):
        product = list_all_orders()
        return Response({'data' : product },status=status.HTTP_200_OK)        

  