from rest_framework import serializers
from store.api.serializers import ProductsSerializer
from cart.models import *
from store.models import *
from django.db.models import Sum

class CartSerializer(serializers.ModelSerializer):
    cartQuantity = serializers.IntegerField(source = "quantity")
    product = ProductsSerializer()
    
    class Meta:
        model = Cart
        fields = ['id','product','user','cartQuantity']

    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['cartCost'] = int(instance.quantity) * int(instance.product.price)
        return representation


class CreateCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    
    class Meta:
        model = Cart
        fields = ['user_id','product_id','quantity']    

class DeleteCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    class Meta:
        model = Cart
        fields = ['product_id']    