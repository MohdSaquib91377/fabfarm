from django.urls import path
from store.api import views
urlpatterns = [
    path('category/', views.CategoryListView.as_view(),name='category_view'),
    path('product/', views.ProductsListView.as_view(),name='product_view'),
    path('product-details/', views.ProductsListView.as_view(),name='product_view'),    
]
