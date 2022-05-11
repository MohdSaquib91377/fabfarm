from unicodedata import category
from rest_framework import serializers

from store.models import *

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image 
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_images")
    category = serializers.CharField(source="category.name", read_only=True)
    brand = serializers.CharField(source="brand.name", read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
        
    def get_images(self, obj):
        images = obj.images.all()
        serializer = ImageSerializer(images,many=True)
        return serializer.data


class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name','products']


