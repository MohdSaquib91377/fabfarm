from django.urls import path
from order.api import views
urlpatterns = [
    path('place-order/', views.OrderAPIView.as_view(),name='place-order'),
    path('order-details/<order_item_id>/', views.OrderDetailsAPIView.as_view(),name='order-details'),
    path('order-cancel/<order_item_id>/', views.OrderCancelAPIView.as_view(),name='order-cancel'),
    path('request-refund-item/',views.RequestRefundItemAPIView.as_view(),name='request-refund-item'),
    path('razorpay/create-fund-account/',views.CreateFundAccountView.as_view(),name = "create-fund-account"),
    path('payout/', views.payout_view,name='payout'),
    path('razorpay/payout/<int:order_item>/', views.RazorpayPayoutAPIView.as_view(),name='razorpay-payout'),


    # Admin Site handle
    path('order-items/',views.GetOrderItemAPIView.as_view(),name = "order-items"),
    path('order-item-details/<int:id>/',views.GetOrderItemDetailAPIView.as_view(),name = 'order-items-details'),
    path('admin-refund/', views.AdminRefund,name='admin-refund'),

    # create contact in razorpay

]
