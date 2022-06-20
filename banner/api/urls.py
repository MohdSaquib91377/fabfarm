from django.urls import path
from banner.api import views

urlpatterns = [
    path('banner/<page_name>/', views.BannerAPIView.as_view(),name='banner-image-or-video'),    

]
    
