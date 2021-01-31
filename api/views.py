from django.shortcuts import render
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from api.data_manager import get_nfl_data as gnd
import requests


class AcmeView(views.APIView):
    def get(self, request):
        req_data = gnd.api_call()
        return Response(req_data, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({"message": "success", "data": request.data}, status=status.HTTP_200_OK)
