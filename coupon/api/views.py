from django.http import Http404
from rest_framework.views import APIView
from .serializers import ApplyCouponSerializer
from coupon.models import *
from rest_framework.response import Response
from coupon.helpers import validate_coupon,apply_coupon_on_cart_total
from rest_framework import permissions

class ApplyCouponApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,coupon_code,*args,**kwargs):
        error_resp = {}
        success,message= validate_coupon(request.user,coupon_code)
        if not success:
            error_resp["message"] = message
            return Response(error_resp, status = 400)

        cart_total,total_amount_payble,discount_amount,coupon_id = apply_coupon_on_cart_total(request.user,message)
        return Response(
            {
            "status":"200",
            "message":"Coupon Applied",
            "data":{
                "coupon_id":coupon_id,
                "cart_total":cart_total,
                "total_amount_payble":total_amount_payble,
                "discounted_price":discount_amount,
            }
            }
            
        )

 