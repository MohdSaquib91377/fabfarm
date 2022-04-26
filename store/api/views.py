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
        catAll = Category.objects.all()
        count = 0
        data =[]
        for category in catAll:
            queryset = category.product_set.all()
    
            serializer = ProductsSerializer(queryset,many=True)
          
            data.append({"category":category.name,"data":serializer.data})
        return Response(data) 
import json
class ProductDetailsView(APIView):
    def get(self,request,product_id,*args, **kwargs):
        queryset = Product.objects.filter(pk=product_id)
        data = []
        categories = CategorySerializer(queryset.first().categories.all(),many=True)

        serializer = ProductsDetailsSerializer(queryset,many=True)
        
        return Response({"category":categories.data,"data":serializer.data}) 