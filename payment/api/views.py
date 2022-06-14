from rest_framework.views import APIView
from .serializers import PaymentSuccessSerializer, PaymentFailureSerializer
from rest_framework.response import Response
from rest_framework import status
from payment.helpers import verify_razorpay_signature,payment_signature_varification,get_razorpay_client,fetch_order_from_razor_pay
from order.models import *
from payment.models import *
from order.helpers import get_order_object
from drf_yasg.utils import swagger_auto_schema

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
            order.order_status = "order_success"
            order.save()
            
            razorpay_order_response = fetch_order_from_razor_pay(razorpay_order_id)
            
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