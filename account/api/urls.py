from django.urls import path
from account.api import views
urlpatterns = [
    path('register/', views.RegisterApiView.as_view(),name='register'),
    path('verify-otp/',views.VerifyOTPApiView.as_view(),name='verify-otp'),
    path('send-otp/',views.SendOTPAPIView.as_view(),name='send-otp'),
    path('login/',views.LoginApiView.as_view(),name='login')
    
   
]
