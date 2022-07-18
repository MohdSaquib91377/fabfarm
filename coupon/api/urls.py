from django.urls import path
from coupon.api import views
urlpatterns = [

    path("apply/<coupon_code>/",views.ApplyCouponApiView.as_view(),name = "coupon-name")

]