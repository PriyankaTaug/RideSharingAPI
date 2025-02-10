from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from RideSharingapp.models import *




class UserTblSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTbl
        fields = '__all__'
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = UserTbl.objects.create(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    username  = serializers.CharField(write_only=True)
    password  = serializers.CharField(write_only=True)

    class Meta:
        model = UserRegisteration
        fields = ['firstname','lastname','phonenumber','usertype','image','username','password']
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self,validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        userreg = UserRegisteration.objects.create(**validated_data)
        UserTbl.objects.create(empid=userreg, username=username,password=password)  # Create UserTbl linked to UserRegisteration
        return userreg
       

   

