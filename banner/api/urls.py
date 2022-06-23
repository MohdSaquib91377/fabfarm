from django.urls import path
from banner.api import views

urlpatterns = [
    path('<page_name>/', views.PageAPIView.as_view(),name='banner-image-or-video'),    

]
    
