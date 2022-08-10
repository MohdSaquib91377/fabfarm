from rest_framework.response import Response
from rest_framework import serializers
from order.models import Order,OrderItem
from account.api.serializers import *
from store.api.serializers import *
from store.models import *

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    coupon = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Order
        fields = ["payment_mode","user","coupon","user_address"]

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

    class Meta:
        model = OrderItem
        fields = "__all__"  
        
