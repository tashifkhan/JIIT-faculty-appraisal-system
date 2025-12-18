from django.shortcuts import render
import logging
from typing import List, Dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from faculty_admin.clients.faculty_data_mongo_client import FacultyDataMongoClient
from django.conf import settings
import json
import urllib.parse
logger = logging.getLogger(__name__)

class GetFacultyData(APIView):
    """
    API Endpoint to get faculty data
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faculty_data_mongo_client = FacultyDataMongoClient()

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get("user_id")

            if not user_id:
                return Response({"message": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            result = self.faculty_data_mongo_client.get_faculty_data_by_user_id(user_id)
            return Response({"message": "Data fetched successfully","result": result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error getting faculty data: {e}")
            return Response({"message": "Error getting faculty data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
