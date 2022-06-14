# dj_razorpay/urls.py

from django.urls import path
from payment import views

urlpatterns = [
	#path('', views.homepage, name='index'),
	path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
	path('payment/', views.checkout, name='checkout'),
	#path('admin/', admin.site.urls),
]
