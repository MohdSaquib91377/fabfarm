from django.urls import path
from order.api import views
urlpatterns = [
    path('place-order/', views.OrderAPIView.as_view(),name='place-order'),
    path('order-details/<order_item_id>/', views.OrderDetailsAPIView.as_view(),name='order-details'),
    path('order-cancel/<order_item_id>/', views.OrderCancelAPIView.as_view(),name='order-cancel'),
    path('cod-request-refund/',views.CodRequestRefundBankInfoCreateView.as_view(),name = 'cod-request-refund'),
    path('code-request-refund-RDU/<int:id>/',views.CodRequestRefundBankInfoRUDView.as_view(),name = 'code-request-refund-RDU'),
    # Admin Site handle
    path('order-items/',views.GetOrderItemAPIView.as_view(),name = "order-items"),
    path('order-item-details/<int:id>/',views.GetOrderItemDetailAPIView.as_view(),name = 'order-items-details'),
    path('admin-refund/', views.AdminRefund,name='admin-refund'),

]
