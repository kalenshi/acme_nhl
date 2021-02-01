from django.shortcuts import render
from rest_framework import status
from rest_framework import views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from api.data_manager import get_nfl_data as gnd
from . import serializers


class AcmeView(views.APIView):
    serializer_class = serializers.InputSerializer

    def get(self, request):
        return Response({"req_data"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                start_date = serializer.validated_data['start_date']
                end_date = serializer.validated_data['end_date']
                req_data = gnd.api_call(start_date, end_date)
                return Response(req_data, status=status.HTTP_200_OK)
        except (TypeError, ValueError, ValidationError) as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
