import re
from rest_framework.response import Response
from order.api.serializers import OrderSerializer,OrderItemSerializer,OrderItemDetailsSerializer,OrderItemIdSerializer,CodRequestRefundSerializer,CodBankSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.utils.crypto import get_random_string
from cart.models import Cart
from order.models import Order, OrderItem,RequestRefundBankInfo
from store.models import *
from cart.helpers import is_product_in_cart
from django.http import Http404
from coupon.helpers import validate_coupon,apply_coupon_on_cart_total
from order.helpers import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from payment.helpers import create_razorpay_order
from order.helpers import update_order_status
from services.email import *
from account.models import *
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

class OrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(tags = ['order'],request_body = OrderSerializer)
    @method_decorator(csrf_exempt, name='dispatch')         
    def post(self,request,*args, **kwargs):
        try:
            print("post-------------------------------->")
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
                    tracking_no = get_random_string(length = 6,allowed_chars = "0123456789"),
                    total_price = cart_total,total_amount_payble = total_amount_payble,discounted_price = discount_amount,coupon = message,
                    user_address = UserAddress.objects.filter(pk = data.get("user_address")).first()
                    )
                    ordered_response["total_price"] = cart_total
                    ordered_response["discount_amount"] = discount_amount
                    ordered_response["total_amount_payble"] = total_amount_payble               
                

                else:
                    cart_total,_ = Cart.get_cart_total_item_or_cost(request.user)
                    order = serializer.save(
                    user = request.user,
                    tracking_no = get_random_string(length = 6,allowed_chars = "0123456789"),
                    total_price = cart_total,total_amount_payble = cart_total,
                    user_address = UserAddress.objects.filter(pk = data.get("user_address")).first()
                    )
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

                    print("product_obj.quantity",product_obj.quantity)
                    print("item.quantity",item.quantity)
                    print("item.product.pk",item.product.pk)

                    product_obj.quantity = product_obj.quantity - item.quantity
                    product_obj.save(update_fields = ["quantity"])

                # Clear User Cart
                Cart.objects.filter(user = request.user).delete()

                # Trigger mail for booking confirmation
                send_mail.delay("You have placed your order","you can check status of your order by using our delivery features,you will receive an order confirmation e-mail with details of your order",[request.user.email_or_mobile])

                return Response(
                    ordered_response
                    ,status = status.HTTP_201_CREATED if is_razor_pay_mode else status.HTTP_200_OK
                    )
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status = 400)

    def get(self,request,*args,**kwargs):
        permission_classes = [permissions.IsAuthenticated]
        try:
            if not Order.objects.filter(user = request.user).exists():
                return Response({"status":"400","message":f"{request.user} your orders not found"},status=status.HTTP_400_BAD_REQUEST)
            current_user_order = Order.objects.filter(user=request.user).first()
            order_list = Order.objects.filter(user=request.user).values_list("id")
            order_queryset = OrderItem.objects.filter(order_id__in = order_list)
            serializer = OrderItemSerializer(order_queryset, many = True)
            return Response(serializer.data,status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status=status.HTTP_400_BAD_REQUEST)



class OrderDetailsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,order_item_id,*args,**kwargs):
        try:    
            if not OrderItem.objects.filter(id = order_item_id).exists():
                return Response({"status":"400","message":"No order found"},status=status.HTTP_400_BAD_REQUEST)
            orderitem_queryset = OrderItem.objects.filter(id = order_item_id)
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
            if order_item.status == "Cancelled":
                return Response({"status":"400","message":"Order item already Cancelled"},status = status.HTTP_400_BAD_REQUEST)
            order_item.status = "Cancelled"
            order_item.save()
            # update product quantity
            product = Product.objects.filter(pk= order_item.product.id).first()
            product.quantity += order_item.quantity
            product.save()

            # update Order status as well
            is_all_items_cancelled = update_order_status(order_item.order.id)
            if is_all_items_cancelled:
                send_mail.delay("your have cancelled your order","We regret to hear of your cancellation. If you are dissatisfied with our customer service, please let us know, and we will connect you with a new agent. We have received your cancellation request. We're sorry to hear you are leaving",[request.user.email_or_mobile])
            else:
                send_mail.delay("your have cancelled some of item from your order","We regret to hear of your cancellation. If you are dissatisfied with our customer service, please let us know, and we will connect you with a new agent. We have received your cancellation request. We're sorry to hear you are leaving",[request.user.email_or_mobile])
            return Response({"status":"200","message":"Order Cancel Successfully"},status = status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status = status.HTTP_400_BAD_REQUEST)


class GetOrderItemAPIView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemIdSerializer

    def get_queryset(self):
        queryset = OrderItem.objects.filter(status = "Request Refund")
        return queryset

class GetOrderItemDetailAPIView(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemDetailsSerializer
    lookup_field = "id"
    

class CodRequestRefundView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CodRequestRefundSerializer
    @swagger_auto_schema(tags = ['order'],request_body = CodRequestRefundSerializer)       
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        item = OrderItem.objects.filter(id = serializer.data["order_item"]).first()
        if not item.status in ["Delivered"]:
            return Response({"status":"400","message":f"order items status should be delivered"},status = 400)
        item.status = "Request Refund"
        RequestRefundBankInfo.objects.filter(id = serializer.data["bank_id"]).update(reason = serializer.data["reason"],order_item = item,order = item.order)
        item.save(update_fields = ["status"])
        return Response({"status":"200","message":f"Your Request has been approved"},status = 200)
    
    
   

class CodBankView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RequestRefundBankInfo.objects.all()
    serializer_class = CodBankSerializer
    
    def perform_create(self,serializer):
        serializer.save(user = self.request.user)

    def get(self,request,*args,**kwargs):
        queryset = RequestRefundBankInfo.objects.filter(user = self.request.user)
        serializer = CodBankSerializer(queryset,many = True).data
        if queryset:
            return Response(serializer)
        return Response({"status":"400","message":"400"},status = 400)


class CodBankRUDView(generics.DestroyAPIView,generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RequestRefundBankInfo.objects.all()
    serializer_class = CodBankSerializer
    lookup_field = "id"
    
  




from django.shortcuts import render

def AdminRefund(request):
    return render(request,"admin-refund.html",{})