
from rest_framework import generics
from .serializers import *
from store.models import *
from order.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from rating_review.api.serializers import (
    ProductRatingSerializer,
)

class ProductRatingView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Rating.objects.all()
    serializer_class =  ProductRatingSerializer

    def post(self,request,*args,**kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            order_item_obj = OrderItem.objects.filter(id = request.data['order_item']).first()
            if not order_item_obj.status in ["Delivered"]:
                return Response({"status":"400","message":"Order item status must be either Delivered or Completed"},status = 400)
            if Rating.objects.filter(product_id=order_item_obj.product_id,user = request.user).exists():
                return Response({"status":"400","message":"Already Rating Reviewed"},status = 400)
            product = Product.objects.filter(id = order_item_obj.product.id).first()
            serializer.save(user=self.request.user,product=product)
            return Response(serializer.data)
        except Exception as e:
            return Response({"status":"400","message":str(e)},status = 400)
            

class ProductRatingDeatilsView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Rating.objects.all()
    serializer_class =  ProductRatingSerializer
    lookup_field = "id"

