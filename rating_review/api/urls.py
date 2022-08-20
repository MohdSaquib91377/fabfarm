from django.urls import path
from rating_review.api import views


urlpatterns = [
    path('product/',views.ProductRatingView.as_view(),name='praduct-rating'),
    path('product-details/<int:id>/',views.ProductRatingDeatilsView.as_view(),name='praduct-rating-details'),


]