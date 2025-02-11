from django.utils import timezone
from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from RideSharingapp.models import RideTbl, UserRegisteration, UserTbl, UserTypeTbl

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_user_registeration(api_client):
    '''Testing the registration of user'''

    # Ensure UserType exists before using it
    user_type, created = UserTypeTbl.objects.get_or_create(type_name="Driver")

    data = {
        "firstname": "Priyanka",
        "username": "priyanka123",
        "password": "securepassword",
        "lastname": "T",
        "usertype": user_type.id,  # Use ID instead of string
        "phonenumber": "9876543210"
    }
    response = api_client.post('/RegisterUser/', data, format="json")

    print("Response Status Code:", response.status_code)
    print("Response Content:", response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == "Success"
    assert response.data["message"] == "User created successfully"
    assert UserTbl.objects.filter(username="priyanka123").exists()



@pytest.fixture
def ride_instance(db):
    """Fixture to create test users and ride instance."""
    user_type, _ = UserTypeTbl.objects.get_or_create(type_name="Driver")
    user_type1, _ = UserTypeTbl.objects.get_or_create(type_name="Rider")

    # Create driver user
    driver_user = UserRegisteration.objects.create(id=1, firstname="Test Driver", usertype=user_type)
    driver_user_id = UserTbl.objects.create(id=1, username="samu@123", password="123", empid=driver_user)
    driver_user_id.save()  # Ensure the instance is committed

    # Create rider user
    rider_user = UserRegisteration.objects.create(id=3, firstname="Test Rider", usertype=user_type1)
    rider_user_id = UserTbl.objects.create(id=2, username="rider@123", password="123", empid=rider_user)
    rider_user_id.save()  # Ensure the instance is committed

    # Create Ride instance
    return RideTbl.objects.create(
        id=1,
        driver=driver_user_id,  # ✅ Assign correct instance
        status=0,
        rider=rider_user_id,  # ✅ Assign correct instance
        created_at=timezone.now()  # ✅ Use timezone-aware datetime
    )

@pytest.mark.django_db
def test_driver_api(api_client, ride_instance):
    """Testing the driver API"""

    data = {
        "id": ride_instance.id,  
        "status": "1"
    }
    response = api_client.patch('/RideRequestAccept/', data, format="json")  # ✅ Use PUT instead of POST

    assert response.status_code == status.HTTP_200_OK  # Adjust based on expected response
    assert response.data["status"] == "Success"
    assert response.data["message"] == "Ride status updated"
