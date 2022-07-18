from django.urls import path
from order.api import views
urlpatterns = [
    path('place-order/', views.OrderAPIView.as_view(),name='place-order'),
    path('order-details/<order_id>/', views.OrderDetailsAPIView.as_view(),name='order-details'),
    path('order-cancel/<order_item_id>/', views.OrderCancelAPIView.as_view(),name='order-cancel'),
]
