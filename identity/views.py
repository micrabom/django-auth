from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"detail": "Not found or Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializers = UserSerializer(instance=user)
        return Response({"token":token.key, "user": serializers.data['username']}, status=status.HTTP_200_OK)

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            token = Token.objects.create(user=user)
            user.set_password(request.data['password'])
            user.save()
            return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class TestTokenView(APIView):
    def get(self, request):
        return Response({"Authorized token!"}, status=status.HTTP_200_OK)
 