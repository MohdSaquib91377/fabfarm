from rest_framework.views import APIView
from store.models import *
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from .serializers import CategorySerializer,ProductsSerializer
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(APIView):    
    def get(self,request,*args, **kwargs):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset,many=True)
        return Response(serializer.data) 

@method_decorator(csrf_exempt, name='dispatch')
class ProductsListView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductsSerializer(queryset,many=True)           
        return Response(serializer.data) 

@method_decorator(csrf_exempt, name='dispatch')
class ProductDetailsView(APIView):
    def get(self,request,product_id,*args, **kwargs):
        queryset = Product.objects.filter(pk=product_id)
        serializer = ProductsSerializer(queryset,many=True)           
        return Response(serializer.data) 
        
@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailsView(APIView):
    def get(self,request,category_id,*args, **kwargs):
        queryset = Product.objects.select_related('category').filter(category_id=category_id)
        serializer = ProductsSerializer(queryset,many=True)
        return Response(serializer.data)