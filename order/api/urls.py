from django.urls import path
from order.api import views
urlpatterns = [
    path('place-order/', views.OrderAPIView.as_view(),name='place-order'),
    path('order-details/<order_item_id>/', views.OrderDetailsAPIView.as_view(),name='order-details'),
    path('order-cancel/<order_item_id>/', views.OrderCancelAPIView.as_view(),name='order-cancel'),
    path('cod-request-refund/',views.CodRequestRefundView.as_view(),name = 'cod-request-refund'),
    path('cod-read-update-delete-bank/<int:id>/',views.CodBankRUDView.as_view(),name = 'cod-read-update-delete-bank'),
    path('create-fund-account/',views.CreateFundAccountView.as_view(),name = "create-fund-account"),
    # Admin Site handle
    path('order-items/',views.GetOrderItemAPIView.as_view(),name = "order-items"),
    path('order-item-details/<int:id>/',views.GetOrderItemDetailAPIView.as_view(),name = 'order-items-details'),
    path('admin-refund/', views.AdminRefund,name='admin-refund'),

    # create contact in razorpay

]
