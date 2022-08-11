from rest_framework.response import Response
from rest_framework import serializers
from order.models import Order,OrderItem,RequestRefundBankInfo
from account.api.serializers import *
from store.api.serializers import *
from store.models import *

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    coupon = serializers.PrimaryKeyRelatedField(read_only = True)
    address = serializers.SerializerMethodField("get_order_address")

    class Meta:
        model = Order
        fields = ["payment_mode","user","coupon","user_address","address"]
    def get_order_address(self,obj):
        serializer = UserAddressSerializer(obj.user_address).data
        return serializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    order = serializers.PrimaryKeyRelatedField(read_only = True)
    payment_mode = serializers.SerializerMethodField("get_order_payment_mode")
    class Meta:
        model = OrderItem
        fields = "__all__"  

    def get_order_payment_mode(self,obj):
        if obj.order.payment_mode in ["COD","cod"]:
            return "Cash on delivery"
        else:
            return "Razorpay"
        
class OrderItemDetailsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    order = OrderSerializer()
    payment_mode = serializers.SerializerMethodField("get_order_payment_mode")
    class Meta:
        model = OrderItem
        fields = "__all__"  

    def get_order_payment_mode(self,obj):
        if obj.order.payment_mode in ["COD","cod"]:
            return "Cash on delivery"
        else:
            return "Razorpay"
# admin side
class OrderItemIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id"]


class CodRequestRefundBankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestRefundBankInfo
        fields = "__all__"