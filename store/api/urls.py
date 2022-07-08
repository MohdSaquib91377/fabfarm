from django.urls import path
from store.api import views
urlpatterns = [
    path('category/', views.CategoryListView.as_view(),name='category-view'),
    path('category-product/', views.CategoryProductView.as_view(),name='category-product'),
    path('category-details/<category_id>/',views.CategoryDetailsView.as_view(),name='category-details'),
    path('parent-category-details/<category_id>/',views.MainCategoryDetailView.as_view(),name='category-details'),
    path('product-details/<product_id>/', views.ProductDetailsView.as_view(),name='product-details'),    
]
