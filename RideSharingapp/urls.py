
from django.urls import path

from RideSharingProject import settings
from RideSharingapp.views import *
from django.conf.urls.static import static

app_name ='RideSharingapp'

urlpatterns = [
  path('rider/',RiderPageView.as_view(),name='RiderPageView'),
  path('RiderDashboardView/',RiderDashboardView.as_view(),name='RiderDashboardView'),
  path('RegisterUser/',RegisterUser.as_view({'post':'create','get':'list'}),name='RegisterUser'),
  path('MatchingAlgorithm/',MatchingAlgorithm.as_view({'get':'list'}),name='MatchingAlgorithm'),
  path('RiderLogin/',RiderLogin.as_view({'post':'create'}),name='RiderLogin'),
  path('RideRequest/',RideRequest.as_view({'post':'create','get':'list'}),name='RideRequest'),
  path('UserRideDetail/<int:id>/',UserRideDetail.as_view({'get':'retrive'}),name='UserRideDetail'),
  path('RideStatusUpdate/<int:id>/',RideStatusUpdate.as_view({'patch':'update'}),name='RideStatusUpdate'),
  path('RideRequestAccept/',RideRequestAccept.as_view({'patch':'update'}),name='RideRequestAccept'),
  path('RegisterRider/',RegisterRider.as_view({'post':'create'}),name='RegisterRider'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)