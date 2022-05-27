from store.models import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

def get_product_object(product_id):
    try:
       return Product.objects.get(id=product_id)
    except Exception as e:
        raise Http404