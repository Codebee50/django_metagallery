from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import UserAccount
from common.responses import SuccessResponse, ErrorResponse
from common.utils import format_first_error
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            try:
                user_obj = UserAccount.objects.get(email=email)
                if not user_obj.is_active:
                    return ErrorResponse(message="Your account has been deactivated, please contact support", status=status.HTTP_401_UNAUTHORIZED)
            except UserAccount.DoesNotExist:
                return ErrorResponse(message="Invalid email or password")
            
            user = authenticate(email=email, password=password)
            if not user:
                return ErrorResponse(message=f"Invalid email or password")
            
            if not user.is_active:
                return ErrorResponse(message="Your account has been disabled, please contact support", status=status.HTTP_401_UNAUTHORIZED)

            
            refresh = RefreshToken.for_user(user)
            return SuccessResponse(
                message="Login successful",
                data={
                    'user': UserSerializer(user).data,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                }
            )
            
        else:
            return ErrorResponse(message=format_first_error(serializer.errors))


class RegisterUserView(generics.GenericAPIView):
    """
    Register a new user
    
    ---
    """
    
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print('user is valid')
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
                        
            UserAccount.objects.create_user(email=email, password=password, username=username)
            return SuccessResponse(message=f'Registration successful')
        else:
            return ErrorResponse(message=format_first_error(serializer.errors))

