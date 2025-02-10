
from django.urls import path

from RideSharingProject import settings
from RideSharingapp.views import *
from django.conf.urls.static import static

app_name ='RideSharingapp'

urlpatterns = [
  path('RegisterUser/',RegisterUser.as_view({'post':'create'}),name='RegisterUser'),
  path('UserLogin/',UserLogin.as_view({'post':'create'}),name='UserLogin'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
