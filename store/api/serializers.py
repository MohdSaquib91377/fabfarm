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
    maxQuantity = serializers.IntegerField(source = "quantity")
    quantity = serializers.SerializerMethodField("set_qauntity_by_1")

    class Meta:
        model = Product
        fields = ["id","name","slug","sku","price","old_price","is_active","is_bestseller","maxQuantity","quantity","description","meta_keywords","meta_description","category","brand","image"]
        
    def get_images(self, obj):
        images = obj.images.all()
        serializer = ImageSerializer(images,many=True)
        return serializer.data

    def set_qauntity_by_1(self,obj):
        return 1

class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name','products']


# Banner Serializer
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
