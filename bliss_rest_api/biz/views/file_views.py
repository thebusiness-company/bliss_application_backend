import os
from django.http import FileResponse
# import pandas as pd
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
import os
from django.http import FileResponse
# import pandas as pd
from ..services.collection_query_service import exec_raw_sql
from ..services.user_service import *
# from ..services.client_service import *
import logging
from ..services.file_service import upload_file, upload_file_as_bytes
# from ..services.address_service import *
from rest_framework.decorators import authentication_classes, permission_classes

logger = logging.getLogger('django')


@authentication_classes([])
@permission_classes([])
class UploadFile(APIView):
    class InputSerializer(serializers.Serializer):
        file = serializers.FileField(required=True)
        source_field = serializers.CharField(required=True)

    def post(self, request):
        # authorize_request('api_upload_file', request.user)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_upd_obj = upload_file('system', **serializer.validated_data)
        return Response({'data': file_upd_obj}, status=status.HTTP_200_OK)

@authentication_classes([])
@permission_classes([])    
class GetFile(APIView):
    class InputSerializer(serializers.Serializer):
        file_path = serializers.CharField(required=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req_file = open(serializer.validated_data.get('file_path'), 'rb')
        response = FileResponse(req_file)
        return response
    
#need to see later.Not necessary now
class GetSelectOptions(APIView):
    class InputSerializer(serializers.Serializer):
        field = serializers.CharField(required=True)
        opt_filter = serializers.JSONField(required=False)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qry_data = serializer.validated_data
        if qry_data.get('opt_filter') is None:
            qry_data.update(opt_filter={})
        res_options = exec_raw_sql(qry_data.get('field'), qry_data.get('opt_filter'))
        return Response({'data': res_options}, status=status.HTTP_200_OK)

