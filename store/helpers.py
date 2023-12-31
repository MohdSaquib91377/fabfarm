from itertools import product
from this import d
from store.models import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from store.api.serializers import *
from io import BytesIO  #basic input/output operation
from PIL import Image #Imported to compress images
from django.core.files import File #to store files

def get_product_object(product_id):
    try:
       return Product.objects.get(id=product_id)
    except Exception as e:
        raise Http404

def add_recent_views_product(user,product_id):
    try:
        recent_views_obj,created = RecentView.objects.get_or_create(user = user,product_id = product_id)
        if not created:
            recent_views_obj.views_counter += 1
            recent_views_obj.save()
        
    except Exception as e:
        print(f"Error -> {e}")


def get_recommed_products(product_id):
    product_obj = get_product_object(product_id)
    product_querysets = Product.objects.select_related("sub_category").filter(sub_category_id = product_obj.sub_category_id)
    product_serializers = ProductsSerializer(product_querysets,many = True)
    return product_serializers.data


def get_product_list(querysets):
    product_object = dict()
    products = list()
    for queryset in querysets:
        for product in queryset["products"]:
                products.append(product)
    return products

