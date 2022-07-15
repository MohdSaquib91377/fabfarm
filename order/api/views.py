from rest_framework.response import Response
from order.api.serializers import OrderSerializer,OrderItemSerializer,OrderItemDetailsSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.utils.crypto import get_random_string
from cart.models import Cart
from order.models import Order, OrderItem
from store.models import *
from cart.helpers import is_product_in_cart
from django.http import Http404
from coupon.helpers import validate_coupon,apply_coupon_on_cart_total
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from payment.helpers import create_razorpay_order
from order.helpers import update_order_status
class OrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(tags = ['order'],request_body = OrderSerializer)
    @method_decorator(csrf_exempt, name='dispatch')         
    def post(self,request,*args, **kwargs):
        try:
            is_razor_pay_mode = False
            ordered_response = dict()
            
            error_resp = {}
            data = json.loads(request.body)
            serializer = OrderSerializer(data = data)
            if serializer.is_valid():
                if not is_product_in_cart(request.user):
                    return Response({"status":"400","message":"No product found in cart"},status=status.HTTP_400_BAD_REQUEST)

                # Created order if couo]pon code provided 
                if data.get('couponCode') != "" and data.get('couponCode') is not None:
                    success,message= validate_coupon(request.user,data.get('couponCode'))
                    if not success:
                        error_resp["message"] = message
                        return Response(error_resp, status = 400)

                    cart_total,total_amount_payble,discount_amount,coupon_id = apply_coupon_on_cart_total(request.user,message)
                    order = serializer.save(
                    user = request.user,
                    tracking_no = data.get('full_name')+get_random_string(length = 6,allowed_chars = "0123456789"),
                    total_price = cart_total,total_amount_payble = total_amount_payble,discounted_price = discount_amount,coupon = message)
                    ordered_response["total_price"] = cart_total
                    ordered_response["discount_amount"] = discount_amount
                    ordered_response["total_amount_payble"] = total_amount_payble               
                

                else:
                    cart_total,_ = Cart.get_cart_total_item_or_cost(request.user)
                    order = serializer.save(
                    user = request.user,
                    tracking_no = data.get('full_name')+get_random_string(length = 6,allowed_chars = "0123456789"),
                    total_price = cart_total,total_amount_payble = cart_total)
                    ordered_response["total_price"] = cart_total

                ordered_response["status"] = "200"
                ordered_response["message"] = "Your ordered has been placed successfully"

                if data.get('payment_mode') == 'razor_pay':
                    is_razor_pay_mode = True
                    razorpay_order_id,order_amount_in_paise,razorpay_key_id = create_razorpay_order(order)
                    ordered_response["razorpay_order_id"] = razorpay_order_id
                    ordered_response["razorpay_key_id"] = razorpay_key_id
                    ordered_response["amount"] = order_amount_in_paise

                
                
                # Read Cart
                user_carts = Cart.objects.filter(user = request.user)

                for item in user_carts:
                    # Create Order Item

                    OrderItem.objects.create(product = item.product, order_id = order.pk,price = item.product.price,quantity=item.quantity)
                  
                    # To Decrease the product quantity from available stock
                    product_obj = Product.objects.filter(pk = item.product.pk).first()
                    product_obj.quantity = product_obj.quantity - item.quantity
                    product_obj.save()

                # Clear User Cart
                Cart.objects.filter(user = request.user).delete()
                return Response(
                    ordered_response
                    ,status = status.HTTP_201_CREATED if is_razor_pay_mode else status.HTTP_200_OK
                    )
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,*args,**kwargs):
        try:
            if not Order.objects.filter(user = request.user).exists():
                return Response({"status":"400","message":f"{request.user} your orders not found"},status=status.HTTP_400_BAD_REQUEST)
            order_queryset = OrderItem.objects.filter()
            serializer = OrderItemSerializer(order_queryset, many = True)
            return Response(serializer.data,status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status=status.HTTP_400_BAD_REQUEST)



class OrderDetailsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,order_id,*args,**kwargs):
        try:    
            if not Order.objects.filter(id = order_id).exists():
                return Response({"status":"400","message":"No order found"},status=status.HTTP_400_BAD_REQUEST)
            orderitem_queryset = OrderItem.objects.filter(order_id = order_id)
            serializer = OrderItemDetailsSerializer(orderitem_queryset,many = True)
            return Response(serializer.data,status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status = status.HTTP_400_BAD_REQUEST)


class OrderCancelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    try:
        def get_object(self,order_item):
            return  OrderItem.objects.filter(pk = order_item).first()
    except Exception as e:
        raise Http404

    def put(self,request,order_item_id,*args,**kwargs):
        try:
            order_item = self.get_object(order_item_id)
            if order_item is None:
                return Response({"status":"400","message":"Order item not found"},status = status.HTTP_400_BAD_REQUEST)
            if order_item.status == "Cancel":
                return Response({"status":"400","message":"Order item already cancel"},status = status.HTTP_400_BAD_REQUEST)
            order_item.status = "Cancel"
            order_item.save()
            # update product quantity
            product = Product.objects.filter(pk= order_item.product.id).first()
            product.quantity += order_item.quantity
            product.save()

            # update Order status as well
            update_order_status(order_item.order.id)

            return Response({"status":"200","message":"Order Cancel Successfully"},status = status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status = status.HTTP_400_BAD_REQUEST)


