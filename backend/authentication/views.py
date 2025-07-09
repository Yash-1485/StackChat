from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, LoginSerializer, OnboardingSerializer, UserSerializer
from .utils.response import error_response, success_response
from .stream import upsert_stream_user
from django.views.decorators.csrf import csrf_exempt
import os

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            if 'email' in errors:
                print(errors)
                email_errors = errors['email']
                
                # Check if any error in the list has 'unique' code - We did it before
                # if any(error.code == 'unique' for error in email_errors):
                #     return error_response("Email already exists", status_code=400,errors=errors)
                
                email_error = errors['email'][0]  # Get first error
                if email_error.code == 'email_exists':  # Our custom code
                    return error_response(
                        str(email_error),  # Using the exact error message
                        status_code=400,
                        errors=errors
                    )
                
                # Check if any error in the list has 'invalid' code
                if any(error.code == 'invalid' for error in email_errors):
                    return error_response("Invalid email address", status_code=400,errors=errors)
            if 'password' in errors and 'min_length' in str(errors['password']):
                return error_response("Password must be at least 8 characters", status_code=400, errors=errors)
            if any(field in errors for field in ['email', 'password', 'fullName']):
                return error_response("All fields are required", status_code=400)
            return error_response("Validation failed", errors=errors, status_code=400)

        user = serializer.save()
        idx = (int.from_bytes(os.urandom(1), 'big') % 100) + 1
        user.profilePic = f"https://avatar.iran.liara.run/public/{idx}.png"
        user.save()

        try:
            upsert_stream_user({
                "id": str(user.id),
                "name": user.fullName,
                "image": user.profilePic
            })
        except Exception as e:
            print(f"Error while creating user to Stream after signup: {str(e)}")
        
        tokens = get_tokens_for_user(user)
        response = Response({
            "success": True,
            "message": "Signup successful",
            "user": UserSerializer(user).data
        }, status=201)

        response.set_cookie(
            key='token',
            value=tokens['access'],
            httponly=True,
            samesite='Strict',
            max_age=7 * 24 * 60 * 60,
        )
        return response
    except Exception as e:
        print(f"Error while signup: {str(e)}")
        return error_response("Internal Server Error", status_code=500,errors=e)
        
# BEFORE: We did it before without using Serializers
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     if not email or not password:
#         return Response({
#             "success": False,
#             "message": "Email and password are required"
#         }, status=400)

#     user = authenticate(email=email, password=password)
#     if not user:
#         return Response({
#             "success": False,
#             "message": "Invalid email or password"
#         }, status=401)

#     tokens = get_tokens_for_user(user)

#     response = Response({
#         "success": True,
#         "message": "Login successful",
#         "user": UserSerializer(user).data
#     }, status=200)

#     response.set_cookie(
#         key='token',
#         value=tokens['access'],
#         httponly=True,
#         samesite='Strict',
#         max_age=7 * 24 * 60 * 60,
#     )
#     return response

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        serializer = LoginSerializer(data=request.data)

        if (not request.data.get('email') or not request.data.get('password')) and (not serializer.is_valid()):
            return error_response("All fields are required", status_code=400,errors=serializer.errors)
        
        if not serializer.is_valid():
            return error_response("Invalid email or password", status_code=401,errors=serializer.errors)

        user = serializer.validated_data["user"]
        tokens = get_tokens_for_user(user)

        response = Response({
            "success": True,
            "message": "Login successful",
            "user": UserSerializer(user).data
        }, status=200)

        response.set_cookie(
            key='token',
            value=tokens['access'],
            httponly=True,
            samesite='Strict',
            max_age=7 * 24 * 60 * 60,
        )
        return response
    except Exception as e:
        print(f"Error while login: {str(e)}")
        return error_response("Internal Server Error", status_code=500,errors=e)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    response = Response({
        "success": True,
        "message": "Logout successful"
    }, status=200)
    response.delete_cookie('token')
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def onboarding(request):
    try:
        user = request.user
        serializer = OnboardingSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():            
            errors=serializer.errors
            if any(field in errors for field in ['fullName','bio','location']):
                return error_response("All fields are required", status_code=400)
            if 'profilePic' in errors and 'invalid' in str(errors['profilePic']):
                return error_response("Invalid profile pic url", status_code=400, errors=errors)
            return Response({
                "success": False,
                "message": "Validation failed while Onboarding",
                "errors": serializer.errors
            }, status=400)

        serializer.save()
        user.isOnboarded = True
        user.save()

        try:
            upsert_stream_user({
                "id": str(user.id),
                "name": user.fullName,
                "image": user.profilePic or ""
            })
        except Exception as e:
            print(f"Error while upserting user to Stream after onboarding: {str(e)}")
        print(f"Stream user updated after onboarding for {user.fullName}")

        return Response({
            "success": True,
            "message": "Onboarding successful",
            "user": UserSerializer(user).data
        }, status=200)
    except Exception as e:
        print(f"Error while onboarding: {str(e)}")
        return error_response("Internal Server Error", status_code=500,errors=e)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        "success": True,
        "user": UserSerializer(request.user).data
    }, status=200)