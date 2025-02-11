from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from RideSharingapp.models import *




class UserTblSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverUserTbl
        fields = '__all__'
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = DriverUserTbl.objects.create(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    username  = serializers.CharField(write_only=True)
    password  = serializers.CharField(write_only=True)

    class Meta:
        model = DriverRegisteration
        fields = ['firstname','lastname','image','username','password']
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self,validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        userreg = DriverRegisteration.objects.create(**validated_data)
        DriverUserTbl.objects.create(driverid=userreg, username=username,password=password)  # Create UserTbl linked to UserRegisteration
        return userreg
       
       
       

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverRegisteration
        fields ='__all__'
        
class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideTbl
        fields ='__all__'

   
class UserTblSerializerData(serializers.ModelSerializer):
    empid = UserDataSerializer()
    class Meta:
        model = DriverUserTbl
        fields = ['empid']
        
class RideDetailSerializer(serializers.ModelSerializer):
    rider = UserTblSerializerData()
    driver = UserTblSerializerData()
    
    class Meta:
        model = RideTbl
        fields ='__all__'
       


class RiderTblSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderUserTbl
        fields = '__all__'
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = RiderUserTbl.objects.create(**validated_data)
        return user


class RiderSerializer(serializers.ModelSerializer):
    username  = serializers.CharField(write_only=True)
    password  = serializers.CharField(write_only=True)

    class Meta:
        model = RiderRegisteration
        fields = ['firstname','lastname','image','username','password']
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self,validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        userreg = RiderRegisteration.objects.create(**validated_data)
        RiderUserTbl.objects.create(riderid=userreg, username=username,password=password)  # Create UserTbl linked to UserRegisteration
        return userreg
       
       