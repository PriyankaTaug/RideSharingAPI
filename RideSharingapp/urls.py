
from django.urls import path

from RideSharingapp.views import RegisterUser

app_name ='RideSharingapp'

urlpatterns = [
  path('RegisterUSer',RegisterUser.as_view({'post':'create'}),name='RegisterUser'),
]
