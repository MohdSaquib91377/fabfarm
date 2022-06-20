from store.models import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

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