from multiprocessing import context
import re
from rest_framework.views import APIView
from store.models import *
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from .serializers import SubCategoryProductSerializer,ProductsSerializer,CategorySerializer,RecentViewProductSerializer,ContactUsSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import generics
# from store.helpers import add_recent_views_product
from rest_framework.permissions import IsAuthenticated
from store.helpers import get_recommed_products,add_recent_views_product,get_product_list
from drf_yasg.utils import swagger_auto_schema


@method_decorator(csrf_exempt, name='dispatch')
class CategoryProductView(APIView):    
    def get(self,request,*args, **kwargs):
        try:
            queryset = SubCategory.objects.all()
            serializer = SubCategoryProductSerializer(queryset,many=True,context={"user":request.user if request.user.id else None})
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
            queryset = Product.objects.select_related('sub_category').filter(sub_category_id=category_id)
            serializer = ProductsSerializer(queryset,many=True,context={"user":request.user if request.user.id else None})
            return Response(serializer.data)

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class ProductDetailsView(APIView):
    def get(self,request,product_id,*args, **kwargs):
        try:

            queryset = Product.objects.filter(pk=product_id)
            serializer = ProductsSerializer(queryset,many=True,context={"user":request.user if request.user.id else None})  
      
            # Query -> Recommend similar products and append to serilizer
            product_recommend_lists = get_recommed_products(product_id)
            data = list(serializer.data)
            data.append({"recommend_products":product_recommend_lists})
            # Add current view product to RecentView model 
            if request.user.id:
                current_user_recent_view_products = request.user.recent_views.select_related("user").filter()
                recent_views_product_serializer = RecentViewProductSerializer(current_user_recent_view_products,many = True).data
                data.append({"recently_views":recent_views_product_serializer})
                add_recent_views_product(request.user,product_id)
            
            return Response(data) 

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)

class MainCategoryDetailView(APIView):
    def get(self,request,category_id,*args,**kwargs):
        queryset = SubCategory.objects.select_related("category").filter(category_id = category_id)
        serializer = SubCategoryProductSerializer(queryset,many=True,context={"user":request.user if request.user.id else None})
        if serializer.data:
            products = get_product_list(serializer.data)
            return Response(products)
        queryset = Product.objects.select_related("category").filter(category_id = category_id)
        serializer = SubCategoryProductSerializer(queryset,many=True,context={"user":request.user if request.user.id else None})
        if serializer.data:
            products = get_product_list(serializer.data)
            return Response(products)
        return Response({"status":"204","message":"Comming Soon"},status = status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(tags = ['store'],request_body = ContactUsSerializer)
class ContactUsAPI(generics.CreateAPIView):
    serializer_class=ContactUsSerializer
    queryset =  ContactUs.objects.all()
    
