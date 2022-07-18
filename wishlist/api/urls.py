from django.urls import path
from wishlist.api import views 
urlpatterns = [
    path('wishlist/add-to-wishlist/',views.WishListAPIView.as_view(),name = "add-to-wishlist")
]