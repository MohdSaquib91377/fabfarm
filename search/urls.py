from django.urls import path
from search import views
urlpatterns = [
path("product/",views.SearchProduct.as_view())
]