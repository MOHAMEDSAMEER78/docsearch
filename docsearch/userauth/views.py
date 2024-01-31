# authentication/views.py

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from datetime import timedelta
from rest_framework.authentication import TokenAuthentication

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    password = data.get('password')
    data.pop('password', None)

    user = User.objects.create_user(**data, password=password)
    user.save()

    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_auth_token(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        response = Response({'token': str(access_token)}, status=status.HTTP_200_OK)

        # Set the access token in an HttpOnly cookie
        response.set_cookie(
            key='access_token',
            value=str(access_token),
            expires=timedelta(minutes=15),  # Set the same expiration as access token
            httponly=True,
            secure=True,  # Set to True in production for secure cookie over HTTPS
        )

        return response
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request):
    # Blacklist the refresh token to invalidate it
    try:
        refresh_token = request.COOKIES.get('access_token')
        RefreshToken(refresh_token).blacklist()
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except:
        response = Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    # Clear the access token cookie
    response.delete_cookie('access_token')

    return response

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_all_users(request):
    users = User.objects.all()
    user_data = [{'id': user.id, 'name': user.name, 'email': user.email, 'dob': user.dob, 'created_at': user.created_at, 'modified_at': user.modified_at} for user in users]
    return Response(user_data, status=status.HTTP_200_OK)
