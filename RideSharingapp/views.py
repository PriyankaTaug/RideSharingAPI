from django.shortcuts import render
from rest_framework import viewsets


# Create your views here.
class RegisterUser(viewsets.ModelViewSet):
    def create(self,request):
        data = request.data('user_data')
