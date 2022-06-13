from rest_framework.views import APIView
from .serializers import PaymentSuccessSerializer, PaymentFailureSerializer
from rest_framework.response import Response
from rest_framework import status
from payment.helpers import verify_razorpay_signature,payment_signature_varification

class PaymentSuccessAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentSuccessSerializer(data=request.data)
        if serializer.is_valid():
            razorpay_payment_id = serializer.data.get('razorpay_payment_id')
            razorpay_order_id = serializer.data.get('razorpay_order_id')
            razorpay_signature = serializer.data.get('razorpay_signature')

            pay_dict = {
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_order_id": razorpay_order_id,
                "razorpay_signature": razorpay_signature
            }
            if not verify_razorpay_signature(pay_dict):
                return Response({"status":"400","message":"Something went wrong while verify razorpay signature"})
            if payment_signature_varification(pay_dict) is None:
                return Response({"status":"200","message":"payment verification success"})
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentFailureAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentFailureSerializer(data=request.data)
        if serializer.is_valid():
            error_code = serializer.data.get('error_code')
            error_description = serializer.data.get('error_description')
            error_source = serializer.data.get('error_source')
            error_step = serializer.data.get('error_step')
            error_reason = serializer.data.get('error_reason')
            error_order_id = serializer.data.get('error_order_id')
            error_payment_id = serializer.data.get('error_payment_id')

           
            return Response({"status":"400","message":"payment failure", "data" :{
                "error_code": error_code,
                "error_description": error_description,
                "error_source": error_source,
                "error_step": error_step,
                "error_description": error_description,
                "error_reason": error_reason,
                "error_order_id": error_order_id,
                "error_payment_id": error_payment_id,
            }}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
