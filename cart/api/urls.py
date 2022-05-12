from django.urls import path
from cart.api import views
urlpatterns = [
    path("add-to-cart/",views.AddToCartApiView.as_view(),name="add-to-cart"),
]
