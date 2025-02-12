from django.utils import timezone
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from RideSharingapp.models import *

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_user_registeration(api_client):
    '''Testing the registration of user'''

   
    data = {
        "firstname": "Priyanka",
        "username": "priyanka123",
        "password": "securepassword",
        "lastname": "T",
        "phonenumber": "9876543210"
    }
    response = api_client.post('/RegisterUser/', data, format="json")

    print("Response Status Code:", response.status_code)
    print("Response Content:", response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == "Success"
    assert response.data["message"] == "User created successfully"
    assert DriverUserTbl.objects.filter(username="priyanka123").exists()



@pytest.fixture
def ride_instance(db):
    """Fixture to create test users and ride instance."""
  

   
    # Create driver user
    driver_user = DriverRegisteration.objects.create(id=1, firstname="Test Driver")

    # Create DriverUserTbl instance (linked to DriverRegisteration)
    driver_user_id = DriverUserTbl.objects.create(id=1, username="samu@123", password="123", driverid=driver_user)

    driver_user_id.save()  

  
    # Create rider user
    rider_user = RiderRegisteration.objects.create(id=3, firstname="Test Rider")

    # Create RiderUserTbl instance (linked to RiderRegisteration)
    rider_user_id = RiderUserTbl.objects.create(id=2, username="rider@123", password="123", riderid=rider_user)
    rider_user_id.save()
    # ✅ Correct assignment in RideTbl (assigning RiderRegisteration instance)
    return RideTbl.objects.create(
        id=1,
        driver=driver_user, 
        status=0,
        rider=rider_user, 
        created_at=timezone.now()
    )


@pytest.mark.django_db
def test_driver_api(api_client, ride_instance):
    """Testing the driver API"""

    data = {
        "id": ride_instance.id,  
        "status": "1"
    }
    response = api_client.patch('/RideRequestAccept/', data, format="json") 

    assert response.status_code == status.HTTP_200_OK 
    assert response.data["status"] == "Success"
    assert response.data["message"] == "Ride status updated"
