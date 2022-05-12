from rest_framework.views import APIView
from store.models import *
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class AddToCartApiView(APIView):
    
    def get(slef,request,*args,**kwargs):
        pass

    def post(self,request,*args,**kwargs):
        pass

    def put(self,request, *args, **kwargs):
        pass
    
    def delete(self,request, *args, **kwargs):
        pass
