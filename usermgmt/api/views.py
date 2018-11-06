# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from usermgmt.backends import JSONWebTokenAuthentication

from ..serializers import (LoginSerializer, PersonalInfoSerializer,
                           UserSerializer)

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            return Response(
                {
                    **serializer.errors,
                    "message": "Invalid request data",
                    "success": False,
                }
            )
        # serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "data": self.serializer_class(user).data,
                "message": "Registration was succsfull.",
                "success": True,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIview(APIView):
    """docstring for LoginAPIview"""

    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    **serializer.errors,
                    "message": "Invalid credentials.",
                    "success": False,
                }
            )

        user = authenticate(**serializer.data)
        if not user:
            return Response(
                {
                    **serializer.errors,
                    "message": "Invalid credentials.",
                    "success": False,
                }
            )
        token = jwt_encode_handler(jwt_payload_handler(user))
        return Response(
            {"message": "Successfully logged in.", "success": True,
             "token": token}
        )


class UserDetailsAPIVew(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        print(type(request.user), "user")
        serializer = self.serializer_class(request.user)
        return Response({"data": serializer.data, "message": "OK",
                         "success": True})


class PersonalInfoAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    personal_info_serializer_class = PersonalInfoSerializer
    user_serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        try:
            personal_info = user.personalinfo
            personal_info_serializer_data = self.personal_info_serializer_class(
                personal_info).data
        except:
            personal_info_serializer_data = {}
        user_serializer_data = self.user_serializer_class(user).data
        return Response({"user_data": user_serializer_data, "personal_data": personal_info_serializer_data, "message": "OK",
                         "success": True}, status=status.HTTP_200_OK)

    def post(self, request):
        request_data = request.data
        user = request.user
        try:
            personal_info = user.personalinfo
            return Response({"success": False,
                             "message": "Personal infor is already created."})
        except:
            personal_info_serializer = self.personal_info_serializer_class(
                data=request_data, context={"user": user})
            if not personal_info_serializer.is_valid():
                return Response({"success": False,
                                 "errors": personal_info_serializer.errors})
            personal_info = personal_info_serializer.save()
            user_serializer_data = self.user_serializer_class(user).data
            return Response(
                {"success": True, "personal_info": request_data,
                 "user_data": user_serializer_data,
                 "message": "Personal info created successfully."})

    def put(self, request):
        request_data = request.data
        user = request.user
        try:
            personal_info = user.personalinfo
            personal_info_serializer = self.personal_info_serializer_class(
                personal_info, data=request_data, context={"user": user})
            if not personal_info_serializer.is_valid():
                return Response({"success": False,
                                 "errors": personal_info_serializer.errors,
                                 "message": "Wrong request data"})
            personal_info = personal_info_serializer.save()
            user_serializer_data = self.user_serializer_class(user).data
            return Response(
                {"success": True, "personal_info": request_data,
                 "user_data": user_serializer_data,
                 "message": "Personal info updated successfully."})
        except:
            return Response({"success": False,
                             "message": "Personal info is not found."})
