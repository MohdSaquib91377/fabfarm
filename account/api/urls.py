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
    path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/',views.ChangePasswordAPIView.as_view(), name='change-password'),
    path("list-update-profile/",views.ListUpdateUpdateProfileAPIView.as_view(), name='create-update-profile'),
    path("update-email/",views.UpdateEmailAPIView.as_view(), name='update-email'),
    path("update-mobile/",views.UpdateMobileAPIView.as_view(), name='update-mobile'),

    # User address urls
    path('user-address/',views.UserAddressListCreateView.as_view(),name = "user-address"),
    path('user-address/<int:pk>/',views.UserAddressDeleteUpdateView.as_view(),name = "user-address")

   
]
