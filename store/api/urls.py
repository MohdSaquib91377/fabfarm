from django.urls import path
from store.api import views
urlpatterns = [
    path('category/', views.CategoryListView.as_view(),name='category-view'),
    path('category-product/', views.CategoryProductView.as_view(),name='category-product'),
    path('category/<category_id>/',views.CategoryDetailsView.as_view(),name='category-details'),
    path('product/<product_id>/', views.ProductDetailsView.as_view(),name='product-details'),    
    path('banner/<page_name>/', views.BannerAPIView.as_view(),name='banner-image-or-video'),    
]
