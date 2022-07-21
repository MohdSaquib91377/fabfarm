from logging import exception
from re import A
from weakref import ref
from rest_framework.views import APIView
from .serializers import PaymentSuccessSerializer, PaymentFailureSerializer,RefundSerializer
from rest_framework.response import Response
from rest_framework import status
from payment.helpers import verify_razorpay_signature,payment_signature_varification,get_razorpay_client,fetch_order_from_razor_pay,create_refund,get_payment_object_by_order_id
from order.models import *
from payment.models import *
from order.helpers import get_order_object
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from payment.models import *

class PaymentSuccessAPIView(APIView):

    @swagger_auto_schema(tags = ['payment'],request_body = PaymentSuccessSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PaymentSuccessSerializer(data=request.data)
        if serializer.is_valid():
            razorpay_payment_id = serializer.validated_data.get('razorpay_payment_id')
            razorpay_order_id = serializer.validated_data.get('razorpay_order_id')
            razorpay_signature = serializer.validated_data.get('razorpay_signature')

            pay_dict = {
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_order_id": razorpay_order_id,
                "razorpay_signature": razorpay_signature
            }
            if not verify_razorpay_signature(pay_dict):
                return Response({"status":"400","message":"Something went wrong while verify razorpay signature"})
            if not payment_signature_varification(pay_dict):
                return Response({"status":"400","message":"payment verification failed"})
            order = get_order_object(razorpay_order_id)
            serializer.save(order = order,user = request.user)

            razorpay_order_response = fetch_order_from_razor_pay(razorpay_order_id)
            order.razorpay_status = razorpay_order_response["status"]
            order.amount_due = razorpay_order_response['amount_due']
            order.amount_paid = razorpay_order_response['amount_paid']
            order.attempts = razorpay_order_response['attempts']
            order.payment_status = "payment_success"
            order.order_status = "order_pending"
            order.save()

            
            
            return Response({
                "status":"200",
                "message":"Payment Verification Successfull"
            },status = status.HTTP_200_OK)
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentFailureAPIView(APIView):
    @swagger_auto_schema(tags = ['payment'],request_body = PaymentFailureSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PaymentFailureSerializer(data=request.data)
        if serializer.is_valid():
            error_code = serializer.validated_data.get('error_code')
            error_description = serializer.validated_data.get('error_description')
            error_source = serializer.validated_data.get('error_source')
            error_step = serializer.validated_data.get('error_step')
            error_reason = serializer.validated_data.get('error_reason')
            error_order_id = serializer.validated_data.get('error_order_id')
            error_payment_id = serializer.validated_data.get('error_payment_id')
            order = get_order_object(error_order_id)
            serializer.save(order = order,user = request.user)
            razorpay_order_response = fetch_order_from_razor_pay(error_order_id)

            order.razorpay_status = razorpay_order_response["status"]
            order.amount_due = razorpay_order_response['amount_due']
            order.amount_paid = razorpay_order_response['amount_paid']
            order.attempts = razorpay_order_response['attempts']
            order.payment_status = "payment_failed"
            order.save()
            return Response({
                "status":"400",
                "message":"payment failed due to inactivity"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RequestRefundAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, order_item,*args, **kwargs):
        try:
            
            serializer = RefundSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            found_order_item = OrderItem.objects.filter(id=order_item).first()
            if not found_order_item:
                return Response({"status":"400","message":"order item not found"},status = 400)

            # Check if order item is develived 
            if not found_order_item.status in ["Delivered"]:
                if found_order_item.status in ["refund_in_progress"]:
                    return Response({"status":"400","message":"Refund in progress"},status =400)
                return Response({"status":"400","message":"Can not refund because order item is not delivered"},status =400)

               # Check if order item is develived 
            if found_order_item.status in ["Refund"]:
                return Response({"status":"400","message":"Can not refund because order item is already refund"},status =400)
            

            # Create Refund and notify razorpay
            refund = create_refund(found_order_item.order,int(found_order_item.product.price)*(found_order_item.quantity))

            '''
            {
            "id": "rfnd_FP8QHiV938haTz",
            "entity": "refund",
            "amount": 500100,
            "receipt": "Receipt No. 31",
            "currency": "INR",
            "payment_id": "pay_29QQoUBi66xm2f",
            "notes": []
            "receipt": null,
            "acquirer_data": {
                "arn": null
            },
            "created_at": 1597078866,
            "batch_id": null,
            "status": "processed",
            "speed_processed": "normal",
            "speed_requested": "normal"
            }
            ''' 
            # Create Refund in Refund Model
            refund_obj = Refund()
            refund_obj.order = found_order_item.order
            refund_obj.order_item = found_order_item
            refund_obj.user = found_order_item.order.user
            refund_obj.payment = Payment.objects.filter(order_id=found_order_item.order.id).first()

            # razorpay responbse
            refund_obj.razorpay_refund_id = refund["id"]
            refund_obj.amount = refund["amount"] / 100
            refund_obj.speed_processed = refund["speed_processed"]
            refund_obj.speed_requested = refund["speed_requested"]
            refund_obj.status = refund["status"]
            refund_obj.save()

            # Update order item status
            found_order_item.status = "refund_in_progress"
            found_order_item.save()

            # Update Order status as well
            order = found_order_item.order
            order.order_status = "partial_order_in_progress"
            order.payment_status = "partial_payment_refund_in_progress"
            order.save()
            return Response({"status": "success","message": f"Refund of Amount <b>INR {int(found_order_item.price):,}</b> has been initiated for Booking ID <b>{order.id}</b>.<br/>Please access the payment gateway to check the respective order for more details."})
        
        except Exception as e:
            return Response({"error":f"{e}"})


