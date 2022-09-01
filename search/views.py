from unittest import result
from django.shortcuts import render

# Create your views here.

from elasticsearch_dsl import Q
from store.documents import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.api.serializers import SearchProductSerializer
from store.documents import ProductDocument
import coreapi

class SearchProduct(APIView):
    serializer_class = SearchProductSerializer
    document_class = ProductDocument
    
    def get(self,request,query):
        try:
            category_id = request.GET.get('category_id')
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            sort_by_asec = request.GET.get('sort_by_asec')
            sort_by_desc = request.GET.get('sort_by_desc')
            if category_id:
                q = Q(
                    "multi_match",
                    query = category_id,
                    fields=["category.id"]
                    )
                search = self.document_class.search().query(q)                      
                search = search.filter('range', price={'gte': min_price, 'lte': max_price})
                if sort_by_asec:
                    search = search.sort(
                        'price'
                    )
                if sort_by_desc:
                    search = search.sort(
                        '-price'
                    )
            else:
                q = Q("multi_match",query = query,fields=["name","brand.name","category.name","sub_category.name","images.image_caption"])
                search = self.document_class.search().query(q)
            queryset = search.to_queryset()
            serializer = self.serializer_class(queryset,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)


    