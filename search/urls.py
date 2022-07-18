from django.urls import path
from search import views
urlpatterns = [
path("product/<str:query>/",views.SearchProduct.as_view())
]