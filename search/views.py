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

class SearchProduct(APIView):
    serializer_class = SearchProductSerializer
    document_class = ProductDocument
    
    def get(self,request,query):
        try:
            q = Q("multi_match",query = query,fields=["name","brand.name","category.name","sub_category.name","images.image_caption"])
            search = self.document_class.search().query(q)
            queryset = search.to_queryset()
            serializer = self.serializer_class(queryset,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)


