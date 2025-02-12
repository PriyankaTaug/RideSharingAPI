from datetime import datetime as dt,timedelta
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from drf_yasg import openapi
from rest_framework import viewsets,status
from rest_framework import status

from rest_framework.response import Response
import logging
from RideSharingapp.models import *
from RideSharingapp.serializer import *
from drf_yasg.utils import swagger_auto_schema
import jwt
from rest_framework.pagination import PageNumberPagination
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


''' Added a login page for Rider '''
class RiderPageView(TemplateView):
    template_name = "login1.html"

'''Login for driver '''
class RiderDashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['driver_data'] = DriverRegisteration.objects.all()  # Pass driver data to the template
        return context


''' Driver Created successfully '''
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
            
                'phonenumber': openapi.Schema(
                    type=openapi.TYPE_STRING, 
            
                ),
                'image':openapi.Schema(type=openapi.TYPE_FILE,description="Upload a profile image (JPEG, PNG, etc.)")
            },
            required=['firstname', 'username', 'password', 'lastname']
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
        

    def list(self,request):
        queryset = DriverRegisteration.objects.all()
        paginator = PaginateRide()
        result_page = paginator.paginate_queryset(queryset, request)
        serial_data = UserDataSerializer(result_page, many=True)
        return paginator.get_paginated_response(serial_data.data)

        


''' After successfull login of rider it will navigate to a dashboard where he/she can see the ride request form '''
class RiderLogin(viewsets.ViewSet):
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
            user_data = RiderUserTbl.objects.get(username=username, password=password)
            user_login_data = {
                'exp': int((dt.now() + timedelta(days=7)).timestamp()),  # Token expiration
                'Name': str(user_data.riderid.firstname),
                'id': str(user_data.riderid.id)
            }

            # Encode access token
            access_token = jwt.encode(user_login_data, 'secret', algorithm='HS256')

            # Encode refresh token
            refresh_token_payload = {
                **user_login_data,
                'refresh_exp': int((dt.now() + timedelta(hours=12)).timestamp()),
            }
            refresh_token = jwt.encode(refresh_token_payload, 'secret', algorithm='HS256')

            response_data = {
                'message': 'Login successful',
                'access': access_token,
                'refresh': refresh_token,
                'id': str(user_data.riderid.id)
            }

            return JsonResponse(response_data, status=200)
        except RiderUserTbl.DoesNotExist:
            return JsonResponse({"message": "Invalid credentials"}, status=400)
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'message': 'Internal server error'}, status=500)



class PaginateRide(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    

''' Ride request add,list '''
class RideRequest(viewsets.ViewSet):
    def list(self,request):
        queryset = RideTbl.objects.all()
        paginator = PaginateRide()
        result_page = paginator.paginate_queryset(queryset, request)
        serial_data = RideSerializer(result_page, many=True)
        return paginator.get_paginated_response(serial_data.data)
        
    def create(self,request):
        ride_data = request.data.copy()
        ride_data['status'] = 0
        try:
            serializer = RideSerializer(data= ride_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':"Success",'message':'User created successfully'},status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response({'status':"Error","message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error",e)
            logger.error(f"Error creating navbar header: {str(e)}")  # Log the error
            return Response({
                "status": "Error",
                "message": "Unexpected error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
''' To  retrieve a particular ride detail''' 
class UserRideDetail(viewsets.ViewSet):
    def retrive(self,request,id=None):
        try:
            ride = RideTbl.objects.get(id = id )
            ride_data = RideDetailSerializer(ride)
            return Response(ride_data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Ride not found"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
''' Ride status update'''      
class RideStatusUpdate(viewsets.ViewSet):
    def update(self,request,id=None):
        try:
            ride_status = request.data.get('status')
            ride = RideTbl.objects.get(id = id )
            ride.status =  ride_status
            ride.save()
            return Response({"success":"Updated ride status"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Ride not found"},status=status.HTTP_404_NOT_FOUND)
        
        
''' Ride request accet by driver'''
class RideRequestAccept(viewsets.ViewSet):
    def update(self, request):
        try:
            id = request.data.get('id')
            if not id:  # ✅ Handle missing ID
                return Response({
                    "status": "Error",
                    "message": "ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            ride_id = RideTbl.objects.get(id=id)
            ride_id.status = 1
            ride_id.save()
            logger.info("Ride status updated successfully")  
            return Response({'status': "Success", 'message': 'Ride status updated'}, status=status.HTTP_200_OK)

        except RideTbl.DoesNotExist:  # ✅ Handle invalid ID
            return Response({
                "status": "Error",
                "message": "Ride not found"
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error updating ride status: {str(e)}")  
            return Response({
                "status": "Error",
                "message": "Unexpected error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RegisterRider(viewsets.ModelViewSet):
    @swagger_auto_schema(
        operation_id='create_user',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'firstname': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
                'lastname': openapi.Schema(type=openapi.TYPE_STRING),
                'phonenumber': openapi.Schema(
                    type=openapi.TYPE_STRING, 
            
                ),
                'image':openapi.Schema(type=openapi.TYPE_FILE,description="Upload a profile image (JPEG, PNG, etc.)")
            },
            required=['firstname', 'username', 'password', 'lastname', 'phonenumber']
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
            serializer = RiderSerializer(data=data)
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
        

    



class MatchingAlgorithm(viewsets.ViewSet):
    def list(self, request):
        try:
            ride_list = RideTbl.objects.all()
            driver_list = DriverRegisteration.objects.filter(is_available=True)
            matches = {}
            assigned_drivers = set()
            for ride in ride_list:
                closest_driver = None
                min_distance = float('inf')
                for driver in driver_list:
                    distance_calc = abs(ride.latitude-driver.latitude) +  abs(ride.longitude-driver.longitude)
                    if distance_calc < min_distance:
                        min_distance = distance_calc
                        closest_driver = driver
                if closest_driver:
                    matches[ride.id] = closest_driver.id
                    assigned_drivers.add(closest_driver.id)
  
            logger.info("Ride status updated successfully")  
            return Response({'status': "Success", 'matches': matches}, status=status.HTTP_200_OK)

        except RideTbl.DoesNotExist:  # ✅ Handle invalid ID
            return Response({
                "status": "Error",
                "message": "Ride not found"
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error updating ride status: {str(e)}")  
            return Response({
                "status": "Error",
                "message": "Unexpected error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
