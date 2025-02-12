from django.db import models

# Create your models here.


class DriverRegisteration(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=50, default=1)
    vehicle_type = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    latitude = models.FloatField(blank=True, null=True)  # Added latitude
    longitude = models.FloatField(blank=True, null=True)  # Added longitude
    image = models.ImageField(upload_to='profile', blank=True, null=True)

class RiderRegisteration(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=50, default=1)
    latitude = models.FloatField(blank=True, null=True)  # Added latitude
    longitude = models.FloatField(blank=True, null=True)  # Added longitude
    image = models.ImageField(upload_to='profile', blank=True, null=True)


class DriverUserTbl(models.Model):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    driverid = models.ForeignKey(DriverRegisteration,on_delete=models.CASCADE,default=1)





class RiderUserTbl(models.Model):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    riderid = models.ForeignKey(RiderRegisteration,on_delete=models.CASCADE,default=1)


class RideTbl(models.Model):
    
    STATUS_CHOICE = [
        (0,'Pending'),
        (1,'Accepted'),
        (2,'Ongoing'),
        (3,'Completed'),
        (4,'Cancelled'),
    ]
    rider = models.ForeignKey(RiderRegisteration,on_delete=models.CASCADE,related_name="rider_data")
    driver = models.ForeignKey(DriverRegisteration,on_delete=models.CASCADE,related_name="driver_data",blank=True,null=True)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICE,default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    