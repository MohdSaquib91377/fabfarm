from asyncio.format_helpers import extract_stack
from rest_framework import serializers
from store.api.serializers import ProductsSerializer
from cart.models import *
from store.models import *
from django.db.models import Sum
from account.api.serializers import *

class CartSerializer(serializers.ModelSerializer):
    cartQuantity = serializers.IntegerField(source = "quantity")
    product = ProductsSerializer()
    user_address = serializers.SerializerMethodField("get_user_address")
    
    class Meta:
        model = Cart
        fields = ['id','product','user','cartQuantity','user_address']

    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['cartCost'] = int(instance.quantity) * int(instance.product.price)
        return representation

    def get_user_address(self,obj):
        user_address_queryset = obj.user.user_address.all() 
        serializer = UserAddressSerializer(user_address_queryset,many = True).data
        return serializer

class CreateCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    class Meta:
        model = Cart
        fields = ['user_id','product_id','quantity']    

class UpdateDeleteCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    action = serializers.CharField(max_length=8)
    class Meta:
        model = Cart
        fields = ['product_id',"action"]    
        extra_kwargs = {"action": {"required": False, "allow_null": True}}
