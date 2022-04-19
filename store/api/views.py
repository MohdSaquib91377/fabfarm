from rest_framework.views import APIView
from store.models import *
from rest_framework.response import Response
from .serializers import CategorySerializer,ProductsSerializer,ProductsDetailsSerializer

class CategoryListView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = Category.objects.all()

        serializer = CategorySerializer(queryset,many=True)
        return Response(serializer.data) 

class ProductsListView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = Product.objects.all()

        serializer = ProductsSerializer(queryset,many=True)
        return Response(serializer.data) 

class ProductDetailsView(APIView):
    def get(self,request,product_id,*args, **kwargs):
        queryset = Product.objects.filter(pk=product_id)

        serializer = ProductsDetailsSerializer(queryset,many=True)
        return Response(serializer.data) 