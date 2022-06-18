from rest_framework.views import APIView
from store.models import *
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from .serializers import CategoryProductSerializer,ProductsSerializer,CategorySerializer,BannerSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import generics
@method_decorator(csrf_exempt, name='dispatch')
class CategoryProductView(APIView):    
    def get(self,request,*args, **kwargs):
        try:

            queryset = Category.objects.all()
            serializer = CategoryProductSerializer(queryset,many=True)
            return Response(serializer.data) 

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)

class CategoryListView(APIView):
    def get(self,request,*args, **kwargs):
        try:

            queryset = Category.objects.all()
            serializer = CategorySerializer(queryset,many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailsView(APIView):
    def get(self,request,category_id,*args, **kwargs):
        try:
            queryset = Product.objects.select_related('category').filter(category_id=category_id)
            serializer = ProductsSerializer(queryset,many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class ProductDetailsView(APIView):
    def get(self,request,product_id,*args, **kwargs):
        try:

            queryset = Product.objects.filter(pk=product_id)
            serializer = ProductsSerializer(queryset,many=True)           
            return Response(serializer.data) 

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)
            
# Banner Api
class BannerAPIView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get_queryset(self):
        page_name = self.kwargs['page_name']
        queryset = Banner.objects.filter(page__icontains = page_name)
        return queryset