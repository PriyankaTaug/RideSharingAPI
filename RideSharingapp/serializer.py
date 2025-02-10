from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'UserRegisteration'
        field = '__all__'
