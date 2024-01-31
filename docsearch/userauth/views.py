# views.py
from django.contrib.auth import get_user_model, login as auth_login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializer import UserSerializer, UserSignupSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User registered successfully", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getallusers(request):
    users = User.objects.all()
    return Response({"users": UserSerializer(users, many=True).data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({"message": "User authenticated successfully", "access_token": str(refresh.access_token)}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid email or password"}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)

