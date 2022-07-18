from django.urls import path
from account.api import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    path('register/', views.RegisterApiView.as_view(),name='register'),
    path('verify-otp/',views.VerifyOTPApiView.as_view(),name='verify-otp'),
    path('send-otp/',views.SendOTPAPIView.as_view(),name='send-otp'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('logout/',views.LogoutAPIView.as_view(),name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
   
]
