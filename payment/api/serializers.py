from rest_framework import serializers
from payment.models import *
class PaymentSuccessSerializer(serializers.Serializer):
    razorpay_payment_id = serializers.CharField(max_length=64)
    razorpay_order_id = serializers.CharField(max_length=64)
    razorpay_signature = serializers.CharField(max_length=64)
    
    def create(self, validated_data):
            return Payment.objects.create(**validated_data)

class PaymentFailureSerializer(serializers.Serializer):
    # Payment Errors
    error_code = serializers.CharField(max_length=128)
    error_description = serializers.CharField(max_length=128)
    error_source = serializers.CharField(max_length=64)
    error_step = serializers.CharField(max_length=64)
    error_reason = serializers.CharField(max_length=64)
    error_order_id = serializers.CharField(max_length=64)
    error_payment_id = serializers.CharField(max_length=64)

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

class RefundSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=128)
    