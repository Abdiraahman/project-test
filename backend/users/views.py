from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserSerializer
from supervisors.serializers import CompanySerializer, CompanyRegistrationSerializer
from django.http import JsonResponse
from django.conf import settings


# class UserRegistrationView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [permissions.AllowAny]
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
        
#         # Generate JWT tokens
#         refresh = RefreshToken.for_user(user)
        
#         return Response({
#             'message': 'User registered successfully',
#             'user': UserSerializer(user).data,
#             'tokens': {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }
#         }, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def login_view(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
    
#     if not email or not password:
#         return Response({
#             'error': 'Email and password are required'
#         }, status=status.HTTP_400_BAD_REQUEST)
    
#     user = authenticate(request, username=email, password=password)
    
#     if user:
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'message': 'Login successful',
#             'user': UserSerializer(user).data,
#             'tokens': {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }
#         })
#     else:
#         return Response({
#             'error': 'Invalid credentials'
#         }, status=status.HTTP_401_UNAUTHORIZED)
# UPDATE your existing login_view function:
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
   
    if not email or not password:
        return Response({
            'error': 'Email and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
   
    user = authenticate(request, username=email, password=password)
   
    if user:
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Create response with user data (no tokens in JSON)
        response_data = {
            'message': 'Login successful',
            'user': UserSerializer(user).data,
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        
        # Set HTTP-only cookies for tokens
        response.set_cookie(
            'access_token',
            str(access_token),
            max_age=60 * 15,  # 15 minutes
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax',
            path='/'
        )
        
        response.set_cookie(
            'refresh_token',
            str(refresh),
            max_age=60 * 60 * 24 * 7,  # 7 days
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax',
            path='/'
        )
        
        return response
    else:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


# UPDATE your existing UserRegistrationView class:
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Create response with user data (no tokens in JSON)
        response_data = {
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
        }
        
        response = Response(response_data, status=status.HTTP_201_CREATED)
        
        # Set HTTP-only cookies for tokens
        response.set_cookie(
            'access_token',
            str(access_token),
            max_age=60 * 15,  # 15 minutes
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax',
            path='/'
        )
        
        response.set_cookie(
            'refresh_token',
            str(refresh),
            max_age=60 * 60 * 24 * 7,  # 7 days
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax',
            path='/'
        )
        
        return response








# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout_view(request):
#     """
#     Robust logout view that blacklists the refresh token
#     """
#     try:
#         refresh_token = request.data.get('refresh_token')
#         if not refresh_token:
#             return Response({
#                 'error': 'Refresh token is required'
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         # Validate that the token belongs to the authenticated user
#         token = RefreshToken(refresh_token)
        
#         # Additional security: verify token belongs to current user
#         if token.payload.get('user_id') != request.user.id:
#             return Response({
#                 'error': 'Token does not belong to authenticated user'
#             }, status=status.HTTP_403_FORBIDDEN)
        
#         token.blacklist()
        
#         return Response({
#             'message': 'Successfully logged out'
#         }, status=status.HTTP_200_OK)
    
#     except TokenError:
#         return Response({
#             'error': 'Invalid or expired token'
#         }, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         # Log the error for debugging (add proper logging)
#         return Response({
#             'error': 'An error occurred during logout'
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# # Add the logout and refresh views to your existing views.py
# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def logout_view(request):
#     response = Response({
#         'message': 'Logged out successfully'
#     }, status=status.HTTP_200_OK)
    
#     # Clear the cookies
#     response.delete_cookie('access_token', path='/')
#     response.delete_cookie('refresh_token', path='/')
    
#     return response


# @api_view(['POST'])  
# @permission_classes([permissions.AllowAny])
# def refresh_token_view(request):
#     refresh_token = request.COOKIES.get('refresh_token')
    
#     if not refresh_token:
#         return Response({
#             'error': 'Refresh token not found'
#         }, status=status.HTTP_401_UNAUTHORIZED)
    
#     try:
#         refresh = RefreshToken(refresh_token)
#         access_token = refresh.access_token
        
#         response = Response({
#             'message': 'Token refreshed successfully'
#         }, status=status.HTTP_200_OK)
        
#         # Set new access token cookie
#         response.set_cookie(
#             'access_token',
#             str(access_token),
#             max_age=60 * 15,  # 15 minutes
#             httponly=True,
#             secure=getattr(settings, 'SECURE_SSL_REDIRECT', False),
#             samesite='Lax',
#             path='/'
#         )
        
#         return response
        
#     except Exception as e:
#         return Response({
#             'error': 'Invalid refresh token'
#         }, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def refresh_token_view(request):
    """
    Refresh access token using refresh token from HTTP-only cookie
    """
    refresh_token = request.COOKIES.get('refresh_token')
    
    if not refresh_token:
        return Response({
            'error': 'Refresh token not found'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Validate and refresh the token
        refresh = RefreshToken(refresh_token)
        new_access_token = refresh.access_token
        
        response_data = {
            'message': 'Token refreshed successfully'
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        
        # Set new access token cookie
        response.set_cookie(
            'access_token',
            str(new_access_token),
            max_age=60 * 15,  # 15 minutes
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax',
            path='/'
        )
        
        return response
        
    except TokenError:
        return Response({
            'error': 'Invalid refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # User must be authenticated
def logout_view(request):
    """
    Logout user by clearing HTTP-only cookies
    """
    response_data = {
        'message': 'Logged out successfully'
    }
    
    response = Response(response_data, status=status.HTTP_200_OK)
    
    # Clear cookies by setting them to expire immediately
    response.set_cookie(
        'access_token',
        '',
        max_age=0,
        httponly=True,
        secure=False,
        samesite='Lax',
        path='/'
    )
    
    response.set_cookie(
        'refresh_token',
        '',
        max_age=0,
        httponly=True,
        secure=False,
        samesite='Lax',
        path='/'
    )
    
    return response



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_status_view(request):
    
    user = request.user
    return Response({
        'profile_completed': user.profile_completed,
        'role': user.role
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    return Response({
        'user': UserSerializer(user).data,
    })


class CompanyRegistrationView(generics.CreateAPIView):
    serializer_class = CompanyRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        
                
        return Response({
            'message': 'Company registered successfully',
            'company': CompanySerializer(company).data,
        }, status=status.HTTP_201_CREATED)

