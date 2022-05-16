from rest_framework.views import APIView
from cart.models import *
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from.serializers import CartSerializer,CreateCartSerializer
from rest_framework import status
from store.helpers import get_product_object
from cart.helpers import *

class AddToCartApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(slef,request,*args,**kwargs):
        try:
            queryset = Cart.objects.filter(user = request.user)
            serializer = CartSerializer(queryset,many=True,context = {'user':request.user})
            cart_total,cart_item = Cart.get_cart_total_item_or_cost(request.user)
            new_serializer_data = list(serializer.data)
            new_serializer_data.append({"cart_total":cart_total,"cart_item":cart_item})
            return Response(new_serializer_data)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status = status.HTTP_400_BAD_REQUEST)

    def post(self,request,*args,**kwargs):
        try:
            if len(request.data) > 0:
                for product in request.data:
                    if isinstance(product,dict):
                        serializer = CreateCartSerializer(data = product)
                        data = product
                        if serializer.is_valid():
                            product = get_product_object(data['product_id'])
                            if int(data['quantity']) < int(product.quantity):
                                if Cart.objects.filter(user = request.user, product = product).exists():
                                    Cart.objects.filter(user = request.user, product = product).update(quantity = data['quantity'])
                                else:
                                    serializer.save(user = request.user) 
                            else:
                                return Response({"status":"400","message":f"You have reach maximum quantity","product_id":product.id},status = status.HTTP_400_BAD_REQUEST)    
                        else:
                            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
                    
                    else:
                        return Response(
                            {"status": "failed", "message": "send data in array of json"},
                            status=400,
                        )   
            else:
                serializer = CreateCartSerializer(data = request.data)
                if not serializer.is_valid():
                    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
            return Response(
                            {"status": "200", "message": "Product Added Into Cart !!"},
                                        status=200,
                                )  
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, *args, **kwargs):
        try:
            product = get_product_object(request.data.get('product_id'))
            user_cart = Cart.objects.filter(user = request.user, product = product).first()
            if user_cart:
                user_cart.delete()
                return Response({"status":"200","message":"Product deleted successfully"},status = status.HTTP_204_NO_CONTENT)
            return Response({"status":"400","message":"You dont have permission to edit this product"},status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status = status.HTTP_400_BAD_REQUEST)