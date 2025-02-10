from datetime import datetime as dt,timedelta
from django.http import JsonResponse
from django.shortcuts import render
from drf_yasg import openapi
from rest_framework import viewsets,status
from rest_framework.response import Response
import logging
from RideSharingapp.models import UserTbl
from RideSharingapp.serializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema
import jwt

logger = logging.getLogger(__name__)

'''' User creation both for driver and rider,the user is diffferentiating by usertype'''

class RegisterUser(viewsets.ModelViewSet):
    @swagger_auto_schema(
        operation_id='create_user',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'firstname': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
                'lastname': openapi.Schema(type=openapi.TYPE_STRING),
                'usertype': openapi.Schema(
                    type=openapi.TYPE_STRING, 
            
                ),
                'phonenumber': openapi.Schema(
                    type=openapi.TYPE_STRING, 
            
                ),
                'image':openapi.Schema(type=openapi.TYPE_FILE,description="Upload a profile image (JPEG, PNG, etc.)")
            },
            required=['firstname', 'username', 'password', 'lastname', 'usertype']
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(description="User created successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(description="Unexpected error"),
        },
    )
    def create(self,request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info("User created successfully") 
                return Response({'status':"Success",'message':'User created successfully'},status=status.HTTP_201_CREATED)
            else:
                return Response({'status':"Error","message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating navbar header: {str(e)}")  # Log the error
            return Response({
                "status": "Error",
                "message": "Unexpected error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UserLogin(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_id='User Login',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(description="Success"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
        },
    )
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user_data = UserTbl.objects.get(username=username, password=password)
            user_login_data = {
                'exp': int((dt.now() + timedelta(hours=24*7)).timestamp()),  # Convert to string
                'role':str(user_data.empid.usertype)
        
            }

            # Generate access token payload with shorter expiry
            access_token_payload = {
                **user_login_data,  # Include user data in the access token payload
            }

            # Encode access token
            access_token_bytes = jwt.encode(access_token_payload, 'secret', algorithm='HS256')
            access_token = access_token_bytes.decode('utf-8') if isinstance(access_token_bytes,
                                                                            bytes) else access_token_bytes

            # Generate refresh token payload with longer expiry
            refresh_token_payload = {
                **user_login_data,
                'refresh_exp': int((dt.now() + timedelta(hours=12)).timestamp()),  # Convert to string
            }
            # Encode refresh token
            refresh_token_bytes = jwt.encode(refresh_token_payload, 'secret', algorithm='HS256')
            refresh_token = refresh_token_bytes.decode('utf-8') if isinstance(refresh_token_bytes,
                                                                              bytes) else refresh_token_bytes

            # Set HTTPOnly flag for cookies and consider Secure flag in production
            response_data = {
                'access': access_token,
                'refresh': refresh_token,
            }
            response = JsonResponse(response_data,safe=False)
            response.set_cookie(key='jwt_access', value=access_token, httponly=True)
            response.set_cookie(key='jwt_refresh', value=refresh_token, httponly=True, samesite='lax')
            # Consider setting the Secure flag based on HTTPS usage in production

            return response
        except UserTbl.DoesNotExist:
            return JsonResponse({"status": "Invalid credentials"}, safe=False)
        except Exception as e:
            print("error", e)
            return JsonResponse({'error': 'Internal server error'}, safe=False)

