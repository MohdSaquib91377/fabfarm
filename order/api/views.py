import re
from rest_framework.response import Response
from order.api.serializers import (OrderSerializer,OrderItemSerializer,OrderItemDetailsSerializer,RequestRefundItemSerializer,
                OrderItemIdSerializer,
                FundAccoutSerializer)
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.utils.crypto import get_random_string
from cart.models import Cart
from order.models import Order, OrderItem,Payout
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


from order.helpers import *
from account.models import Contact,FundAccout

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
    

class CreateFundAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FundAccoutSerializer

    @swagger_auto_schema(tags = ['order'],request_body = FundAccoutSerializer)
    def post(self,request,*args, **kwargs):

        try:
            # create contact
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception = True)
            if not request.user.contact.filter().exists():
                data = {
                "name": request.user.fullname,
                "email": request.user.email_or_mobile,
                "type":"customer",
                "reference_id":f"{request.user.fullname}{request.user.id}"
                }
                if request.user.mobile:
                    data["contact"] = request.user.mobile

                response,status = create_contact("contacts",data)
                if status == 201:
                    Contact.objects.create(user = request.user,razorpay_conatct_id = response["id"])

            #Create Fund Account
            data = {
                "contact_id":request.user.contact.filter().first().razorpay_conatct_id,
                "account_type":"bank_account",
                "bank_account":{
                    "name":serializer.data["name"],
                    "ifsc":serializer.data["ifsc"],
                    "account_number":serializer.data["account_number"],
                }

            }
            response,status= create_fund_account("fund_accounts",data)
            if status == 201:
                FundAccout.objects.create(
                                    user = request.user,
                                    razorpay_fund_id = response["id"],
                                    account_type = response["account_type"],
                                    contact_id = response["contact_id"],
                                    ifsc = response["bank_account"]["ifsc"],
                                    bank_name = response["bank_account"]["bank_name"],
                                    account_number = response["bank_account"]["account_number"],
                                    name = response["bank_account"]["name"],
                                    active = response["active"],
                                    )

                return Response({"status":"200","message":"Your account has been created successfully"},status=200)
    

        except Exception as e:
            return Response({"status":"400","message":e},status=400)

    def get(self,request, *args, **kwargs):
        queryset = FundAccout.objects.filter(user = request.user)
        print(queryset)
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data) 


class RequestRefundItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RequestRefundItemSerializer
    @swagger_auto_schema(tags = ['order'],request_body = RequestRefundItemSerializer)
    def post(self,request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception = True)

            order_item = OrderItem.objects.filter(id = serializer.validated_data["order_item"].id).first()
            if not order_item.status in ["Delivered"]:
                return Response({"status":"400","message":"Order item is not delivered"},status=400)
            
            serializer.save(user = request.user)
            order_item.status = "Request Refund"
            order_item.save(update_fields = ["status"])
            return Response({"status":"200","message":"Your request has been approved"},status=200)
        except Exception as e:
            return Response({"status":"400","message":e},status=400)


class RazorpayPayoutAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def post(self, request, order_item,*args, **kwargs):
        try:
            # create razorpay payout 
            order_item = OrderItem.objects.filter(id = order_item).first()
            if not order_item.is_return:
                return Response({"status":"400","message":"Order item is not return"},status=400)
            if Payout.objects.filter(order_item=order_item,status = "processed").exists():
                return Response({"status":"400","message":"Order item is already payout"},status=400)

            data = {
                "account_number": settings.ACCOUNT_NUMBER,
                "fund_account_id": order_item.refund_items.filter().first().fund_accounts.razorpay_fund_id,
                "amount": int(order_item.product.price * order_item.quantity)*100,
                "currency": "INR",
                "mode": "IMPS",
                "purpose": "refund",
                "queue_if_low_balance": True,
                "reference_id": "Acme Transaction ID 12345",
                "narration": "Acme Corp Fund Transfer"
                }
            response,status = create_payout("payouts",data)
            if status == 200:
                Payout.objects.create(
                    
                        order_item = order_item,
                        order = order_item.order,
                        razorpay_payout_id = response["id"],
                        fund_account_id = response["fund_account_id"],
                        amount = response["amount"]/100,
                        currency = response["currency"],
                        fees = response["fees"],
                        tax = response["tax"],
                        status = response["status"],
                        purpose = response["purpose"],
                        utr = response["utr"],
                        mode = response["mode"],    
                        reference_id = response["reference_id"],
                        merchant_id = response["merchant_id"],


                )
                return Response({"status":"200","message":"Payout created"},status=200)
            return Response({"status":f"{status}","message":f"{response['error']['description']}"},status=status)
            
                
        except Exception as e:
            return Response({"status":"400","message":f"{e}"},status = 400)           
   


from payment.helpers import *
class RazorpayPayoutWebhooksAPIView(APIView):
    def post(self, request, *args, **kwargs):
        webhook_body = request.body.decode("utf-8")
        webhook_signature = request.headers["X-Razorpay-Signature"]
        webhook_secret = settings.RAZORPAY_WEBHOOK_KEY_SECRET
        client = get_razorpay_client()
        if not client.utility.verify_webhook_signature(webhook_body, webhook_signature, webhook_secret):
            return Response({"status":400,"message":"not authorized webhook"})
        json_data = json.loads(webhook_body)
        if json_data["event"] in ["payout.processed"]:
            update_payout(json_data["payload"]["payout"]["entity"])

        elif json_data["event"] in ["payout.reversed"]:
            update_payout(json_data["payload"]["payout"]["entity"])

        
        return Response({"status":"200","message":"Payout webhooks get called"},status=200)

  
from django.shortcuts import render

def AdminRefund(request):
    return render(request,"admin-refund.html",{})

def payout_view(request):
    return render(request, 'payout.html', {})


