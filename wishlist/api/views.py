from bdb import Breakpoint
from rest_framework.views import APIView 
from wishlist.models import Wishlist
from .serializers import WishListSerializer,WishListCreateDeleteSerializer
from store.models import Product
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class WishListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,*args, **kwargs):
        queryset = Wishlist.objects.filter(user = request.user)
        serializer = WishListSerializer(queryset,many = True)
        return Response(serializer.data,status = 200)

    @swagger_auto_schema(tags = ['wishlist'],request_body = WishListCreateDeleteSerializer)
    def post(self,request,*args, **kwargs):
        serializer = WishListCreateDeleteSerializer(data = request.data)
        product = Product.objects.filter(id = request.data['product_id']).first()
        serializer.is_valid(raise_exception = True)
        found_wishlist = Wishlist.objects.filter(product = product,user=request.user).first()
        if found_wishlist:
            found_wishlist.delete()
            return Response({"status":"200","message":"Product removed from wishlist"},status=201)

        serializer.save(user = self.request.user,product = product)
        return Response({"status": "200","message":"Product added into wishlist"},status =200)
    
    @swagger_auto_schema(tags = ['wishlist'],request_body = WishListCreateDeleteSerializer)
    def delete(self,request,*args, **kwargs):       
        serializer = WishListCreateDeleteSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        product = Product.objects.filter(id = request.data['product_id']).first()
        if Wishlist.objects.filter(product = product,user = request.user).exists():
            Wishlist.objects.filter(product = product,user = request.user).delete()
            return Response({"status": "200","message":"Product removed from wishlist"},status = 203)
        return Response({"status": "400","message":"You dont have permission to remove product from wishlist"},status = 400)