
from rest_framework import serializers
from coupon.models import Coupon

class ApplyCouponSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coupon
        fields = ["couponCode"]