from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from payment import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Ecommerce API",
      default_version='v1',
      description="Test description",
),
   url='https://fab-farm.datavivservers.in/api/v1/',
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='index'),
    path('',include('payment.urls')),
    path('api/v1/store/',include('store.api.urls')),
    path('api/v1/account/',include('account.api.urls')),
    path('api/v1/cart/',include('cart.api.urls')),
    path('api/v1/order/',include('order.api.urls')),
    path('api/v1/coupon/',include('coupon.api.urls')),
    path('api/v1/wishlist/',include('wishlist.api.urls')),
    path('api/v1/payment/',include('payment.api.urls')),
    path('api/v1/banner/',include('banner.api.urls')),
    path('api/v1/search/',include('search.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




