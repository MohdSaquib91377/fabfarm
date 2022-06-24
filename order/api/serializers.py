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
        fields = ["full_name","city","state","country","pincode","locality","landmark","address","alternate_number","payment_mode","message","user","coupon"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    order = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = OrderItem
        fields = "__all__"  

class OrderItemDetailsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    order = OrderSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"  
