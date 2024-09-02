from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from rest_framework import status
from ..services.product_service import *
from ..models import *
from rest_framework.decorators import authentication_classes, permission_classes
from django.utils import timezone 
import datetime


class AddProduct(APIView):
    class InputSerializer(serializers.Serializer):
        product_name = serializers.CharField()
        product_image = serializers.ListField()
        description = serializers.CharField()
        original_price = serializers.IntegerField()
        selling_price = serializers.IntegerField()
        quantity =serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = create_product(request.user.username,**serializer.validated_data)

        return Response({'data' : product },status=status.HTTP_200_OK)
           
@authentication_classes([])
@permission_classes([])        
class GetProduct(APIView):
    class InputSerializer(serializers.Serializer):
        # product_name = serializers.CharField()
        product_id = serializers.CharField()
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_product(**serializer.validated_data)
        return Response({'data' : product },status=status.HTTP_200_OK)

@authentication_classes([])
@permission_classes([]) 
class ListProduct(APIView):
    def get(self, request):
        product = list_products()
        return Response({'data' : product },status=status.HTTP_200_OK)

class UpdateProduct(APIView):
    class InputSerializer(serializers.Serializer):
        product_id = serializers.CharField()
        product_name = serializers.CharField()
        product_image = serializers.ListField()
        description = serializers.CharField()
        original_price = serializers.IntegerField()
        selling_price = serializers.IntegerField()
        quantity = serializers.IntegerField()
        trending= serializers.BooleanField()
        availability=serializers.BooleanField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = update_product(request.user.username,**serializer.validated_data)
        return Response({'data' : product },status=status.HTTP_200_OK)

class DeleteProduct(APIView):
    class InputSerializer(serializers.Serializer):
        # product_name = serializers.CharField()
        product_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = delete_product(**serializer.validated_data)

        return Response({'data' : product },status=status.HTTP_200_OK)        