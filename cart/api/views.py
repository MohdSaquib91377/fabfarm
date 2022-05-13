from rest_framework.views import APIView
from cart.models import *
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from.serializers import CartSerializer,CreateCartSerializer
from rest_framework import status
from store.helpers import get_product_object

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
            serializer = CreateCartSerializer(data = request.data)
            product = get_product_object(request.data.get('product_id'))
            if serializer.is_valid():
                if Cart.objects.filter(user = request.user, product = product).exists():
                    Cart.objects.filter(user = request.user, product = product).update(quantity = serializer.data['quantity'])
                    return Response({"sttaus":"200","message":"Product updated into Cart"},status = status.HTTP_400_BAD_REQUEST)
                serializer.save(user = request.user)
                return Response({"sttaus":"200","message":"Product Added into Cart"},status = status.HTTP_201_CREATED)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status= status.HTTP_400_BAD_REQUEST)

    def put(self,request, *args, **kwargs):
        try:
            product = get_product_object(request.data.get('product_id'))
            user_cart = Cart.objects.filter(user = request.user, product = product).first()
            if user_cart:
                serializer = CreateCartSerializer(user_cart,data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status":"200","message":"Product updated into cart successfully"},status = status.HTTP_200_OK)
                return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
            return Response({"status":"400","message":"You dont have permission to edit this product"},status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status = status.HTTP_400_BAD_REQUEST)

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