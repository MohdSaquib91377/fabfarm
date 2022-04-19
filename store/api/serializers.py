from rest_framework import serializers

from store.models import *
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"



class ProductsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"