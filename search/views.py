from unittest import result
from django.shortcuts import render

# Create your views here.

# from elasticsearch_dsl import Q
from django.db.models import Q
from store.documents import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.api.serializers import SearchProductSerializer
from store.documents import ProductDocument
import coreapi
from rating_review.helpers import *
from elasticsearch_dsl.query import MoreLikeThis
from django.conf import settings
class SearchProduct(APIView):
    serializer_class = SearchProductSerializer
    document_class = ProductDocument
    
    def get(self,request):
        category_id = request.GET.get('category_id')
        sub_category_id = request.GET.get('sub_category_id')
        search = request.GET.get('search')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        sort_by_asec = request.GET.get('sort_by_asec')
        sort_by_desc = request.GET.get('sort_by_desc')
        sort_by_popularity = request.GET.get('sort_by_popularity')
        
        if settings.ELASTICSEARCH in ['true','True',True]:
            if category_id and search:
                q = Q("multi_match",query = search,fields=["name","brand.name","category.name","sub_category.name","images.image_caption"], fuzziness='auto')
                search = self.document_class.search().query(q)
                search = search.filter('term',category__id = category_id)

            elif sub_category_id and search:
                q = Q("multi_match",query = search,fields=["name","brand.name","category.name","sub_category.name","images.image_caption"], fuzziness='auto')
                search = self.document_class.search().query(q)
                search = search.filter('term',sub_category__id = sub_category_id)
            
            elif category_id:
                q = Q('bool',must = [Q('match',category__id = category_id)],minimum_should_match=1)
                search = self.document_class.search().query(q)
                
            elif sub_category_id:
                q = Q('bool',must = [Q('match',sub_category__id = sub_category_id)],minimum_should_match=1)
                search = self.document_class.search().query(q)


            # sort product based on range
            if min_price != 0 and max_price !=0:
                search = search.filter('range', price={'gte': min_price, 'lte': max_price})

            # sort product based on asecending order
            if sort_by_asec in ["true"]:
                search = search.sort(
                    'price'
                )

            # sort product based on desecending order
            if sort_by_desc in ["true"]:
                search = search.sort(
                    '-price'
                )
            

            # filter product based on popularity
            if sort_by_popularity in ['true']:
                queryset = search.to_queryset()
                sorted_order_id = get_sort_by_popularity(queryset)
                queryset = sorted(search.to_queryset(), key=lambda x: sorted_order_id.index(x.id)) 

            queryset = search.to_queryset()
            serializer = self.serializer_class(queryset,many=True)
            return Response(serializer.data)

        else:
            if category_id and search:
                # q = Q("multi_match",query = search,fields=["name","brand.name","category.name","sub_category.name","images.image_caption"], fuzziness='auto')
                search = Product.objects.filter(
                    Q(name__icontains=search) |
                    Q(brand__name__icontains=search) |
                    Q(category__name__icontains=search) |
                    Q(sub_category__name__icontains=search)
                    )
                search = search.filter(category__id = category_id)

            elif sub_category_id and search:
                search = Product.objects.filter(
                    Q(name__icontains=search) |
                    Q(brand__name__icontains=search) |
                    Q(category__name__icontains=search) |
                    Q(sub_category__name__icontains=search)
                    )
                search = search.filter(sub_category__id = sub_category_id)
            
            elif category_id:
                search = Product.objects.filter(category__id = category_id)

            elif sub_category_id:
                search = Product.objects.filter(sub_category__id = sub_category_id)


            # sort product based on range
            if int(min_price) != 0 and int(max_price) !=0:
                search = search.filter(Q(price__gte= min_price)&Q(price__lte=max_price))

            # sort product based on asecending order
            if sort_by_asec in ["true"]:
                search = search.order_by('price')

            # sort product based on desecending order
            if sort_by_desc in ["true"]:
                search = search.order_by(
                    '-price'
                )
            

            # filter product based on popularity
            if sort_by_popularity in ['true']:
                sorted_order_id = get_sort_by_popularity(search)
                queryset = sorted(search, key=lambda x: sorted_order_id.index(x.id)) 

            serializer = self.serializer_class(search,many=True)
            return Response(serializer.data)




    