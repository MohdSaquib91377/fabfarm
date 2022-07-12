from django.urls import path
from payment.api import views

urlpatterns = [
    path('payment-success/',views.PaymentSuccessAPIView.as_view(),name='payment-sucess'),
    path('payment-failure/',views.PaymentFailureAPIView.as_view(),name='payment-failure')

]